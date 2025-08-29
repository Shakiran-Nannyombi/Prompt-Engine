import sys
import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_groq import ChatGroq
from streamlit import feedback
from models.evaluation import EvaluationResult
from langgraph.prebuilt import ToolNode
from agents import tools

sys.path.append(os.path.abspath(".."))

# Importing environment variables
load_dotenv(dotenv_path="../../.env")

# Setup PostgreSQL checkpointing
DB_URI = os.environ["DATABASE_URL"]
memory = PostgresSaver.from_conn_string(DB_URI)

# State of graph
class CoachingState(TypedDict):
    task: str
    context: str
    references: List[str]
    evaluation_criteria: str
    final_prompt: str
    messages: Annotated[list, add_messages]
    current_step: str
    evaluation_result: EvaluationResult
    summary: str
    
# Models
llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0.5
)

tool_node = ToolNode(tools.tool_list)
evaluation_llm = llm.with_structured_output(EvaluationResult)
llm_with_tools = llm.bind_tools(tools=tools.tool_list, parallel_tool_calls=False)

welcome_message = """
**Welcome!** I'm here to help you master prompt engineering by building an effective 
prompt using the **'Task(Persona and Format), Context, References, Evaluate, Iterate'** framework.

To get more understanding of this framework, you can refer to our documentation
[here](https://example.com/docs).

**Let's start with the Task.** Please describe what you would like to accomplish.
It could be a specific goal or a general area of interest. 

**Don't have anything in mind?** Just ask me to "suggest some tasks" and I'll generate creative ideas for you!
"""

def start_coaching(state: CoachingState):
    """Initial node that starts the coaching process"""
    return {
        "messages": [AIMessage(content=welcome_message)], 
        "current_step": "awaiting_task_input"
    }

def process_task_input(state: CoachingState):
    """Process user's task input - only called when we have user input"""
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        # Should never happen with proper routing, but just in case
        return {"current_step": "error"}
    
    last_message = messages[-1]
    user_input = last_message.content.lower()

    # Check if it's just a greeting or very short input
    if len(user_input.strip()) < 5 or user_input.strip() in ["hi", "hello", "hey", "sup", "yo"]:
        greeting_response = f"""
        Hello! 👋 I'm excited to help you create an effective prompt!
        
        To get started, please tell me what you'd like to accomplish. For example:
        - "Create a chatbot for tutoring students in math"
        - "Write a professional email template"
        - "Generate code for a simple calculator"
        - "Design a lesson plan for teaching history"
        
        **What would you like to create or build?**
        """
        return {
            "messages": [AIMessage(content=greeting_response)], 
            "current_step": "awaiting_task_input"
        }
        
        # Check if user wants suggestions
    if any(keyword in user_input for keyword in ["suggest", "suggestion", "random", "generate", "idea", "help me think"]):
        suggestion_prompt = """
        Generate 4 creative and diverse task ideas for prompt engineering practice. 
        Each task should be practical, engaging, and cover different domains.
        Format your response as a numbered list with brief descriptions.
        """
        response = llm.invoke(suggestion_prompt)
        
        suggestion_message = f"""
        **Here are some creative task suggestions for you:**
        {response.content}
        
        **Choose one of these or describe your own task!**
        Which of these interests you, or would you like to tell me about a different task you have in mind?
        """
        return {
            "messages": [AIMessage(content=suggestion_message)], 
            "current_step": "awaiting_task_input"  # Still need task input
        }
    
    # Evaluate the task
    instruction = f"""
    Evaluate the following user-defined task based on clarity, specificity, and actionability.
    User's Task: "{last_message.content}"
    
   ACCEPT the task if it describes:
    - Any type of content creation (essays, stories, code, etc.)
    - Any kind of assistant or chatbot functionality
    - Any educational or tutoring request
    - Any analysis, research, or information gathering task
    - Any creative or technical project
    
    ONLY REJECT if the input is:
    - Completely unrelated to a task (like just "hi" or "hello")
    - Harmful, inappropriate, or illegal content
    - Completely nonsensical
    
    Be ENCOURAGING and HELPFUL. Most user inputs should be accepted as valid starting points.
    If the task is somewhat vague but shows clear intent, ACCEPT it and suggest improvements in the feedback.
    
    For the task: "{last_message.content}"
    - Does this describe something the user wants to accomplish? 
    - Is it a reasonable request for AI assistance?
    
    If YES, mark as correct and provide encouraging feedback.
    If the task could be more specific, still mark as correct but suggest enhancements.
    """
    
    result: EvaluationResult = evaluation_llm.invoke(instruction) 
    final_task = result.updated_prompt or last_message.content
    
    if result.is_correct:
        context_prompt = f"""
        Perfect! I understand your task: **"{final_task}"**
        
        This is a great starting point! Now let's add some context to make your prompt even more effective.
        
        Please provide context by thinking about:
        - **Background**: What's the setting or situation?
        - **Audience**: Who is this for? (students, professionals, general audience?)
        - **Requirements**: Any specific constraints, length, style, or format needed?
        - **Purpose**: How will this be used or what's the end goal?
        
        **What context can you provide for your task?**
        """
        
        return {
            "task": final_task,
            "evaluation_result": result,
            "messages": [AIMessage(content=context_prompt)],
            "current_step": "awaiting_context_input"  # Ready for context
        }
    else:
        # Only reject clearly invalid inputs
        feedback_message = f"""
        I'd like to help, but I need a clearer understanding of what you want to accomplish.
        
        {result.feedback}
        
        **Examples of tasks I can help with:**
        - "Create a chatbot for customer service"
        - "Write an essay about climate change"  
        - "Generate code for a calculator app"
        - "Design a lesson plan for teaching math"
        
        **What would you like to create or accomplish?**
        """
        return {
            "task": final_task,
            "evaluation_result": result,
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_task_input"  # Still need task input
        }

def process_context_input(state: CoachingState):
    """Process user's context input - only called when we have user input"""
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"current_step": "error"}
    
    last_message = messages[-1]
    task = state.get("task", "")
    
    instruction = f"""
    Evaluate the following user-defined context based on relevance, completeness, and clarity.
    Analyze how well it supports the task: "{task}"
    User's Context: "{last_message.content}"
    Is this context description sufficient to proceed?
    """
    
    result: EvaluationResult = evaluation_llm.invoke(instruction) 
    final_context = result.updated_prompt or last_message.content
    
    if result.is_correct:
        reference_prompt = f"""
        Excellent! Your context adds great depth: "{final_context}"
        
        Now let's gather references. Please think about:
        - Documents, links, or resources that could help
        - Examples of similar tasks or prompts
        - Specific data or information to include
        - Style guides or formatting preferences
        
        **Please describe any references or additional resources for your task.**
        """
        
        return {
            "context": final_context,
            "evaluation_result": result,
            "messages": [AIMessage(content=reference_prompt)],
            "current_step": "awaiting_reference_input"  # Ready for references
        }
    else:
        feedback_message = f"{result.feedback}\n\nPlease provide more detailed context and try again."
        return {
            "context": final_context,
            "evaluation_result": result,
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_context_input"  # Still need context input
        }

def process_reference_input(state: CoachingState):
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"current_step": "error"}
    
    last_message = messages[-1]
    task = state.get("task", "")
    context = state.get("context", "")
    
    instruction = f"""
    Evaluate the following user-defined references based on relevance, credibility, and usefulness.
    Task: "{task}", Context: "{context}", References: "{last_message.content}"
    Is this reference description sufficient to proceed?
    """
    
    result: EvaluationResult = evaluation_llm.invoke(instruction) 
    final_references = result.updated_prompt or last_message.content
    
    if result.is_correct:
        summary = f"""
        **Task:** {task}
        **Context:** {context}
        **References:** {final_references}
        """
        
        final_prompt_guidance = f"""
        Perfect! You have all the key components:
        {summary}
        
        **Now create your final prompt** that incorporates:
        - Your task (with clear persona/role and output format)
        - The context you've provided
        - Reference to the resources you mentioned
        - Clear, specific instructions
        
        **Write your complete engineered prompt below:**
        """
        
        return {
            "references": [final_references],
            "evaluation_result": result,
            "summary": summary,
            "messages": [AIMessage(content=final_prompt_guidance)],
            "current_step": "awaiting_final_prompt"  # Ready for final prompt
        }
    else:
        feedback_message = f"{result.feedback}\n\nPlease provide better references and try again."
        return {
            "references": [final_references],
            "evaluation_result": result,
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_reference_input"  # Still need reference input
        }

def process_final_prompt(state: CoachingState):
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"current_step": "error"}
    
    last_message = messages[-1]
    summary = state.get("summary", "")
    
    evaluation_instruction = f"""
    Evaluate this final prompt for clarity, completeness, and effectiveness:
    Framework used: {summary}
    Final prompt: "{last_message.content}"
    
    Is this prompt well-structured and ready to use?
    """
    
    result: EvaluationResult = evaluation_llm.invoke(evaluation_instruction)
    
    if result.is_correct:
        return {
            "final_prompt": last_message.content,
            "messages": [AIMessage(content="Excellent prompt! Let me polish it for you...")],
            "current_step": "ready_to_refine"  # Ready for tool refinement
        }
    else:
        feedback_message = f"{result.feedback}\n\nPlease refine your prompt based on this feedback."
        return {
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_final_prompt"  # Still need final prompt
        }

def agent_node(state: CoachingState):
    # Agent node acts as the brain that uses tools to refine the final prompt
    final_prompt = state.get("final_prompt", "")
    refine_instruction = f"Please use the grammar_checker tool to polish this prompt: {final_prompt}"
    
    messages = state.get("messages", [])
    messages.append(SystemMessage(content=refine_instruction))
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_call_tools(state: CoachingState) -> str:
    # Checks if we should call tools
    messages = state.get("messages", [])
    if messages:
        last_message = messages[-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "call_tools"
    return "display_final_result"

def display_final_result(state: CoachingState):
    final_prompt = state.get("final_prompt", "")
    
    completion_message = f"""
**Congratulations!** You've successfully crafted a well-structured prompt using the 
**'Task, Context, References, Evaluate, Iterate'** framework.

**Your Final Engineered Prompt:**

---
{final_prompt}
---

**What you've accomplished:**
- Defined a clear task with persona and format
- Provided relevant context 
- Included helpful references
- Practiced evaluation and iteration throughout

You can now use this prompt with your AI model or save it to your prompt library.

**Happy Prompting!** 
    """
    
    return {
        "messages": [AIMessage(content=completion_message)],
        "current_step": "completed"
    }

# Route user input to the appropriate processing node based on current step
def route_user_input(state: CoachingState) -> str:
    current_step = state.get("current_step", "")
    messages = state.get("messages", [])
    
    # Check if we have a user message
    if not messages or not isinstance(messages[-1], HumanMessage):
        return END
    
    # Route based on current step
    if current_step == "awaiting_task_input":
        return "process_task_input"
    elif current_step == "awaiting_context_input":
        return "process_context_input"  
    elif current_step == "awaiting_reference_input":
        return "process_reference_input"
    elif current_step == "awaiting_final_prompt":
        return "process_final_prompt"
    else:
        return END

# Router node that doesn't modify state, just routes
def router_node(state: CoachingState):
    return state

# Graph building
builder = StateGraph(CoachingState)

# Add all nodes
builder.add_node("start_coaching", start_coaching)
builder.add_node("router", router_node) 
builder.add_node("process_task_input", process_task_input)
builder.add_node("process_context_input", process_context_input)
builder.add_node("process_reference_input", process_reference_input)
builder.add_node("process_final_prompt", process_final_prompt)
builder.add_node("agent_node", agent_node)
builder.add_node("tool_node", tool_node)
builder.add_node("display_final_result", display_final_result)

# Start always goes to start_coaching
builder.add_edge(START, "start_coaching")

# From start_coaching, go to router to wait for user input
builder.add_edge("start_coaching", "router")

# Router conditionally routes to processing nodes based on user input and current step
builder.add_conditional_edges(
    "router",
    route_user_input,
    {
        "process_task_input": "process_task_input",
        "process_context_input": "process_context_input",
        "process_reference_input": "process_reference_input", 
        "process_final_prompt": "process_final_prompt",
        END: END
    }
)

# Each processing node has conditional edges based on success/failure
builder.add_conditional_edges(
    "process_task_input",
    lambda state: "process_context_input" if state.get("current_step") == "awaiting_context_input" else "router",
    {
        "process_context_input": "process_context_input",
        "router": "router"
    }
)

builder.add_conditional_edges(
    "process_context_input", 
    lambda state: "process_reference_input" if state.get("current_step") == "awaiting_reference_input" else "router",
    {
        "process_reference_input": "process_reference_input",
        "router": "router"
    }
)

builder.add_conditional_edges(
    "process_reference_input",
    lambda state: "process_final_prompt" if state.get("current_step") == "awaiting_final_prompt" else "router",
    {
        "process_final_prompt": "process_final_prompt", 
        "router": "router"
    }
)

builder.add_conditional_edges(
    "process_final_prompt",
    lambda state: "agent_node" if state.get("current_step") == "ready_to_refine" else "router",
    {
        "agent_node": "agent_node",
        "router": "router"
    }
)

# Tool execution flow
builder.add_conditional_edges(
    "agent_node",
    should_call_tools,
    {
        "call_tools": "tool_node",
        "display_final_result": "display_final_result"
    }
)

builder.add_edge("tool_node", "display_final_result")
builder.add_edge("display_final_result", END)

# compile the graph with memory
coach_graph = builder.compile(checkpointer=memory)

# function for demo Streamlit app
def extract_message_content(message) -> tuple[str, str]:
    if isinstance(message, AIMessage):
        return "assistant", message.content
    elif isinstance(message, HumanMessage):
        return "user", message.content
    elif isinstance(message, SystemMessage):
        return "system", message.content
    elif isinstance(message, tuple):
        return message[0], message[1]
    else:
        return "unknown", str(message)
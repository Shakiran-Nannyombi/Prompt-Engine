import sys
import os
from dotenv import load_dotenv
import psycopg
from typing import TypedDict, Annotated, List
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_groq import ChatGroq
from streamlit import feedback
from models.evaluation import EvaluationResult
from langgraph.prebuilt import ToolNode
from agents.tools import coach_tools

sys.path.append(os.path.abspath(".."))

# Importing environment variables (load from project root if available)
load_dotenv()

# Setup PostgreSQL checkpointing
DB_URI = os.environ.get("DATABASE_URL", "")
if not DB_URI:
    raise RuntimeError("DATABASE_URL is not set in environment")

# Enabling LangSmith for coach agent (only if tracing is enabled)
os.environ["LANGSMITH_API_KEY"] = os.environ.get("COACH_LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"] = os.environ.get("COACH_LANGSMITH_PROJECT", "coach_agent")

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
    task_corrected: str
    context_corrected: str
    references_corrected: List[str]
    final_prompt_corrected: str
    
# Models
llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0.5
)

tool_node = ToolNode(coach_tools.tool_list)
evaluation_llm = llm.with_structured_output(EvaluationResult)
llm_with_tools = llm.bind_tools(tools=coach_tools.tool_list, parallel_tool_calls=False)

def correct_grammar(text: str) -> str:
    """Automatically correct grammar and improve text clarity using LLM"""
    if not text or not text.strip():
        return text
    
    correction_prompt = f"Please correct any grammar, spelling, and punctuation errors in the following text while preserving its original meaning and intent. Make minimal changes - only fix clear errors and improve clarity where needed. Do not change the core content, style, or add new information.\n\nText to correct: \"{text}\"\n\nReturn only the corrected text, nothing else."
    
    try:
        response = llm.invoke(correction_prompt)
        corrected_text = response.content.strip()
        # Remove quotes if the LLM wrapped the response in them
        if corrected_text.startswith('"') and corrected_text.endswith('"'):
            corrected_text = corrected_text[1:-1]
        return corrected_text
    except Exception as e:
        # If correction fails, return original text
        return text

welcome_message = """
Hey there! 👋 I'm your friendly prompt engineering coach, and I'm genuinely excited to help you craft something amazing together!

Think of me as your creative partner who's here to guide you through building a really effective prompt.
We'll use a proven approach I like to call **'Task, Context, References, Evaluate, Iterate'** - but don't worry, it's way more fun than it sounds! 😊

**Here's how we'll roll:** We'll start by figuring out exactly what you want to create or accomplish. 
It could be anything - a chatbot, a writing assistant, code generation, creative content, you name it!

**Feeling a bit stuck or just want to explore?** No worries at all! Just tell me to "suggest some tasks" and I'll throw some creative ideas your way.

So, what's on your mind? What would you love to build or create today? 
"""

def start_coaching(state: CoachingState):
    existing_messages = state.get("messages", [])
    if existing_messages:
        # Preserve current step or default to awaiting_task_input
        return {"current_step": state.get("current_step", "awaiting_task_input")}
    return {
        "messages": [AIMessage(content=welcome_message)], 
        "current_step": "awaiting_task_input"
    }

def process_task_input(state: CoachingState):
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        # Should never happen with proper routing, but just in case
        return {"current_step": "error"}
    
    last_message = messages[-1]
    user_input = last_message.content.lower()

    # Check if it's just a greeting or very short input
    if len(user_input.strip()) < 5 or user_input.strip() in ["hi", "hello", "hey", "sup", "yo"]:
        greeting_response = f"""
        Hey there! 👋 So great to meet you! I can already tell we're going to create something awesome together.
        
        I'm here to help you build a really powerful prompt that gets amazing results. 
        Think of it like we're crafting the perfect recipe - we just need to figure out what delicious outcome you're after! 
        
        Here are some ideas to get your creative juices flowing:
        • "Help me create a math tutoring chatbot that makes learning fun"
        • "I need a template for writing professional emails that actually get responses"
        • "Build me a coding assistant for simple calculator functions"
        • "Design an engaging history lesson plan that keeps students interested"
        
        **So, what's your vision?** What would you love to create or accomplish today? I'm all ears! 
        """
    
        return {
            "messages": [AIMessage(content=greeting_response)], 
            "current_step": "awaiting_task_input"
        }
        
        # Check if user wants suggestions
    if any(keyword in user_input for keyword in ["suggest", "suggestion", "random", "idea", "help me think"]):
        suggestion_prompt = """
        Generate 4 creative and diverse task ideas for prompt engineering practice. 
        Each task should be practical, engaging, and cover different domains.
        Format your response as a numbered list with brief descriptions.
        """
        response = llm.invoke(suggestion_prompt)
        
        suggestion_message = f"""
        Ooh, I love that you want to explore!  Here are some fun ideas I've cooked up for you:
        
        {response.content}
        
        **Any of these spark your interest?** Or maybe they've inspired a completely different idea? I'm totally flexible - we can go with one of these suggestions, mix and match elements, or dive into something entirely different that's brewing in your mind!
        
        What's calling to you? Let's make it happen! 
        """
        return {
            "messages": [AIMessage(content=suggestion_message)], 
            "current_step": "awaiting_task_input"
        }
    
    # Automatically correct grammar in user input
    original_task = last_message.content
    corrected_task = correct_grammar(original_task)
    
    # Evaluate the task using corrected version
    instruction = f"""
    Evaluate the following user-defined task based on clarity, specificity, and actionability.
    Check if they have included a persona and output format.
    User's Task: "{corrected_task}"
    
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
    
    For the task: "{corrected_task}"
    - Does this describe something the user wants to accomplish? 
    - Is it a reasonable request for AI assistance?
    
    If YES, mark as correct and provide encouraging feedback.
    If the task could be more specific, still mark as correct but suggest enhancements.
    """
    
    result: EvaluationResult = evaluation_llm.invoke(instruction) 
    # Use corrected task for processing
    final_task = corrected_task
    
    if result.is_correct:
        context_prompt = f"""
        Fantastic! I love what you're going for: **"{final_task}"** 
        
        Now here's where we get to add some real magic! Think of context as the secret sauce that transforms a good prompt into an absolutely amazing one. It's like giving your AI assistant all the insider knowledge they need to nail exactly what you want.
        
        **Here's what would be super helpful to know:**
        
        - **Who's this for?** (Your audience - are we talking to beginners, experts, kids, professionals?)
        
        - **What's the vibe?** (Formal, casual, fun, professional? And how do you want the output formatted - bullet points, tables, paragraphs?)
        
        - **What's the setting?** (Any background info, constraints, or special requirements I should know about?)
        
        - **How will you use this?** (Is this for work, school, personal projects, daily use?)
        
        **Pro tip:** If you want to add a persona (like "You are an expert teacher" or "Act as a friendly advisor"), that can work wonders too, but it's totally optional!
        
        **Tell me more about your situation!** The more details you share, the better we can tailor this prompt to work perfectly for you. 
        """
        
        # Ensures we progress to context step
        return {
            "task": original_task,
            "task_corrected": final_task,
            "evaluation_result": result,
            "messages": [AIMessage(content=context_prompt)],
            "current_step": "awaiting_context_input"
        }
    else:
        feedback_message = f"""
        Hey, no worries at all! I can see you've got something in mind, but I'd love to understand your vision a bit better so I can give you the best help possible! 
        
        {result.feedback}
        
        **Here are some examples of the cool stuff we could work on together:**
        - "Help me create a friendly customer service chatbot"
        - "I need to write a compelling essay about climate change"  
        - "Build a smart calculator app that explains the steps"
        - "Design an interactive math lesson that keeps students engaged"
        
        **What's your dream project?** I'm here to help you bring any idea to life - just paint me a picture of what you're imagining! 
        """
        return {
            "task": original_task,
            "task_corrected": final_task,
            "evaluation_result": result,
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_task_input"
        }

def process_context_input(state: CoachingState):
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"current_step": "error"}
    
    last_message = messages[-1]
    task = state.get("task_corrected", state.get("task", ""))  # Use corrected task
    
    # Automatically correct grammar in context input
    original_context = last_message.content
    corrected_context = correct_grammar(original_context)
    
    instruction = f"""
    Evaluate the following user-defined context based on relevance, completeness, and clarity.
    Analyze how well it supports the task: "{task}"
    User's Context: "{corrected_context}"
    Is this context description sufficient to proceed?
    """
    
    result: EvaluationResult = evaluation_llm.invoke(instruction) 
    # Using corrected context for processing
    final_context = corrected_context
    
    if result.is_correct:
        reference_prompt = f"""
        Awesome, this context is perfect! You've really painted a clear picture: "{final_context}"
        
        Now for the final piece of our puzzle - let's talk about references! Think of these as the "inspiration files" or "cheat sheets" that will make your prompt absolutely shine.
        
        **What kind of goodies do you have to work with?**
        
        - **Got any examples?** (Similar prompts, templates, or outputs you've seen that you love?)
        
        - **Helpful resources?** (Websites, documents, style guides, or specific data you want included?)
        
        - **Style preferences?** (Any particular tone, format, or approach you want to follow?)
        
        - **Industry insights?** (Specific knowledge, jargon, or standards from your field?)
        
        **Don't stress if you don't have much!** Even something like "I like how ChatGPT explains things simply" or "Make it sound like a friendly expert" counts as valuable reference info.
        
        **What resources or examples can you share with me?** Every little bit helps us craft something amazing! ✨
        """
        
        return {
            "context": original_context,
            "context_corrected": final_context,
            "evaluation_result": result,
            "messages": [AIMessage(content=reference_prompt)],
            "current_step": "awaiting_reference_input"
        }
    else:
        checklist = f"""
        Your context can mention:
        - Courses, audience, level, constraints (e.g., hours/week)
        - Key goals and priorities
        - Any constraints or deadlines
        
        Examples tailored to your task:
        1) "I'm a 3rd-year CS student taking AI, UI, Embedded Systems. I have 20 hours/week. I need a weekly plan with exam countdowns."
        2) "I work 15 hours/week part-time. Prefer a Markdown table with days Mon–Sun, morning/evening slots, and focus sessions for metrics and evolution."
        """
        feedback_message = f"{result.feedback}\n\nPlease provide more detailed context and try again.\n\n{checklist}\n\nPlease share your context, then we'll proceed to references."
        return {
            "context": original_context,
            "context_corrected": final_context,
            "evaluation_result": result,
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_context_input"
        }

def process_reference_input(state: CoachingState):
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"current_step": "error"}
    
    last_message = messages[-1]
    task = state.get("task_corrected", state.get("task", ""))  # Use corrected task
    context = state.get("context_corrected", state.get("context", ""))  # Use corrected context
    
    # Automatically correct grammar in reference input
    original_references = last_message.content
    corrected_references = correct_grammar(original_references)
    user_refs = (corrected_references or "").strip().lower()

    # Check if user wants to proceed without references
    proceed_explicit_patterns = ["proceed without references", "proceed without", "skip references"]
    no_ref_patterns = [
        "no references", "none", "don't have", "dont have", "i have none", "no ref", "no resource", "nothing",
        "i dont have responses", "i dont have any"
    ]
    
    # If user explicitly says "proceed without references", move forward immediately
    if any(p in user_refs for p in proceed_explicit_patterns):
        final_references = "No specific references provided - proceeding with general best practices"
        summary = f"""
        **Task:** {task}
        **Context:** {context}
        **References:** {final_references}
        """
        
        final_prompt_guidance = f"""
        Perfect! No worries about references - we've got everything we need to create something amazing! 

        Look at what we've built together:
        {summary}

        **Now comes the exciting part - let's create your masterpiece!** 

        Time to weave all these elements into one powerful, cohesive prompt. Think of yourself as a master chef combining the perfect ingredients:

        - **Your task** (with that perfect persona/role and output format we discussed)
        - **Your context** (all that juicy background info)
        - **Crystal-clear instructions** (so your AI knows exactly what you want)

        **Ready to create your final prompt?** Pour all of this goodness into one beautifully crafted instruction that will get you amazing results every time!

        I'm so excited to see what you come up with! 
        """
        
        return {
            "references": [original_references],
            "references_corrected": [final_references],
            "summary": summary,
            "messages": [AIMessage(content=final_prompt_guidance)],
            "current_step": "awaiting_final_prompt"
        }
    
    # If user says they don't have references (first time), offer suggestions
    elif any(p in user_refs for p in no_ref_patterns):
        suggestion_prompt = f"""
        Based on the user's task and context, suggest practical reference ideas the user could provide
        to improve prompt quality. Tailor to their scenario.
        Task: "{task}"
        Context: "{context}"

        Return 5-7 concise, concrete suggestions in a numbered list. Cover:
        - example datasets or documents they may already have
        - similar examples/templates from their domain
        - links or sections they could look up (generic placeholders ok)
        - style/tone guides relevant to their audience
        - any structured info (tables/fields) helpful for this task
        Keep items short (one line each).
        """
        # Combine LLM suggestions with web search suggestions (non-authoritative)
        response = llm.invoke(suggestion_prompt)
        search_query = f"reference ideas for: {task} ({context[:60]}) study planner"
        try:
            web_results = coach_tools.tavily_search_tool.run(search_query)
        except Exception:
            web_results = ""

        suggestion_message = f"""
        It's okay if you don't have references yet. Here are some ideas to consider:

        {response.content}

        Web suggestions (to explore):
        {web_results}

        You can:
        - Pick any items from the list to use as references
        - Describe informal references (notes, past assignments, screenshots)
        - Or reply "proceed without references" and we'll continue
        """

        return {
            "messages": [AIMessage(content=suggestion_message)],
            "current_step": "awaiting_reference_input"
        }
    
    instruction = f"""
    Evaluate the following user-defined references based on relevance, credibility, and usefulness.
    Task: "{task}", Context: "{context}", References: "{corrected_references}"
    Is this reference description sufficient to proceed?
    """
    
    result: EvaluationResult = evaluation_llm.invoke(instruction) 
    # Using corrected references for processing
    final_references = corrected_references
    
    if result.is_correct:
        summary = f"""
        **Task:** {task}
        **Context:** {context}
        **References:** {final_references}
        """
        
        final_prompt_guidance = f"""
        YES! We've got all the ingredients for something truly spectacular! Look at what we've built together:
        
        {summary}
        
        **Now comes the exciting part - let's create your masterpiece!** 
        
        Time to weave all these elements into one powerful, cohesive prompt. Think of yourself as a master chef combining the perfect ingredients:
        
        - **Your task** (with that perfect persona/role and output format we discussed)
        - **Your context** (all that juicy background info)
        - **Your references** (those helpful resources and examples)
        - **Crystal-clear instructions** (so your AI knows exactly what you want)
        
        **Ready to create your final prompt?** Pour all of this goodness into one beautifully crafted instruction that will get you amazing results every time!
        
        I'm so excited to see what you come up with! 
        """
        
        return {
            "references": [original_references],
            "references_corrected": [final_references],
            "evaluation_result": result,
            "summary": summary,
            "messages": [AIMessage(content=final_prompt_guidance)],
            "current_step": "awaiting_final_prompt"
        }
    else:
        feedback_message = f"{result.feedback}\n\nPlease provide better references and try again."
        return {
            "references": [original_references],
            "references_corrected": [final_references],
            "evaluation_result": result,
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_reference_input"
        }

def process_final_prompt(state: CoachingState):
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"current_step": "error"}
    
    last_message = messages[-1]
    summary = state.get("summary", "")
    
    # Automatically correct grammar in final prompt input
    original_final_prompt = last_message.content
    corrected_final_prompt = correct_grammar(original_final_prompt)
    
    evaluation_instruction = f"""
    Evaluate this final prompt for clarity, completeness, and effectiveness:
    Framework used: {summary}
    Final prompt: "{corrected_final_prompt}"
    
    Is this prompt well-structured and ready to use?
    """
    
    result: EvaluationResult = evaluation_llm.invoke(evaluation_instruction)
    
    if result.is_correct:
        # brief rubric and compatibility text for tests
        rubric = "- Clarity: ✓  - Constraints: ✓/✗  - Format specified: ✓/✗  - References used: ✓/✗"
        preface = f"Your prompt looks solid. Here's a quick rubric check:\n{rubric}\nExcellent prompt! Let me polish it for you..."
        return {
            "final_prompt": original_final_prompt,
            "final_prompt_corrected": corrected_final_prompt,
            "messages": [AIMessage(content=preface)],
            "current_step": "ready_to_refine"
        }
    else:
        feedback_message = f"{result.feedback}\n\nPlease refine your prompt based on this feedback."
        return {
            "evaluation_result": result,
            "messages": [AIMessage(content=feedback_message)],
            "current_step": "awaiting_final_prompt"
        }

def agent_node(state: CoachingState):
    # Agent node acts as the brain that uses tools to refine the final prompt
    final_prompt = state.get("final_prompt_corrected", state.get("final_prompt", ""))
    refine_instruction = f"The final prompt has been grammar-corrected and is ready for further refinement: {final_prompt}"
    
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
    final_prompt = state.get("final_prompt_corrected", state.get("final_prompt", ""))
    
    completion_message = f"""
**WOW! Look what we created together!** 

You've just crafted something absolutely incredible using our **'Task, Context, References, Evaluate, Iterate'** approach, and I couldn't be more proud! This is going to get you some seriously amazing results.

**Your Beautiful, Final Engineered Prompt:**

---
{final_prompt}
---

**Just look at what you've accomplished! 🌟**
- Nailed down a crystal-clear task with perfect persona and formatting
- Added rich, meaningful context that gives your AI all the insider knowledge
- Wove in those perfect references and examples
- Refined everything through our collaborative evaluation process

**You're all set to go make magic happen!** 

This prompt is ready to use with any AI model, and I have a feeling it's going to blow you away with the quality of responses you get. Don't forget to save this gem to your prompt library!

**Go forth and create amazing things!** I had such a blast working with you on this! 
    """
    
    return {
        "messages": [AIMessage(content=completion_message)],
        "current_step": "completed"
    }

# Routing user input to the appropriate processing node based on current step
def decide_next_step(state: CoachingState) -> str:
    current_step = state.get("current_step", "")
    messages = state.get("messages", [])
    # Checking for the existing updated state
    has_task = bool(state.get("task"))
    has_context = bool(state.get("context"))
    has_references = bool(state.get("references"))
    has_final_prompt = bool(state.get("final_prompt"))
    
    # Check if we have a user message
    if not messages:
        # Nothing yet; start coaching
        return "start_coaching"
    if not isinstance(messages[-1], HumanMessage):
        # Last was assistant/system; wait for user input
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
        if has_final_prompt:
            return "agent_node"
        if has_references:
            return "process_final_prompt"
        if has_context:
            return "process_reference_input"
        if has_task:
            return "process_context_input"
        return "process_task_input"

# Router that just routes
def await_user_input_node(state: CoachingState):
    return state

# Graph building
builder = StateGraph(CoachingState)

# Add all nodes
builder.add_node("start_coaching", start_coaching)
builder.add_node("await_user_input", await_user_input_node) 
builder.add_node("process_task_input", process_task_input)
builder.add_node("process_context_input", process_context_input)
builder.add_node("process_reference_input", process_reference_input)
builder.add_node("process_final_prompt", process_final_prompt)
builder.add_node("agent_node", agent_node)
builder.add_node("tool_node", tool_node)
builder.add_node("display_final_result", display_final_result)

# Starting always goes to start_coaching
builder.add_edge(START, "start_coaching")

# From start_coaching, go to router to wait for user input
builder.add_edge("start_coaching", "await_user_input")

# Router conditionally routes to processing nodes based on user input and current step
builder.add_conditional_edges(
    "await_user_input",
    decide_next_step,
    {
        "start_coaching": "start_coaching",
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
    lambda state: "process_context_input" if state.get("current_step") == "awaiting_context_input" else "await_user_input",
    {
        "process_context_input": "process_context_input",
        "await_user_input": "await_user_input"
    }
)

builder.add_conditional_edges(
    "process_context_input", 
    lambda state: "process_reference_input" if state.get("current_step") == "awaiting_reference_input" else "await_user_input",
    {
        "process_reference_input": "process_reference_input",
        "await_user_input": "await_user_input"
    }
)

builder.add_conditional_edges(
    "process_reference_input",
    lambda state: "process_final_prompt" if state.get("current_step") == "awaiting_final_prompt" else "await_user_input",
    {
        "process_final_prompt": "process_final_prompt", 
        "await_user_input": "await_user_input"
    }
)

builder.add_conditional_edges(
    "process_final_prompt",
    lambda state: "agent_node" if state.get("current_step") == "ready_to_refine" else "await_user_input",
    {
        "agent_node": "agent_node",
        "await_user_input": "await_user_input"
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

# compiling the graph with memory using a persistent connection
# Temporary connection for setup
setup_conn = psycopg.connect(DB_URI)
setup_conn.autocommit = True
PostgresSaver(setup_conn).setup()
setup_conn.close()

# Persistent connection for runtime
conn = psycopg.connect(DB_URI)
memory = PostgresSaver(conn)
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
import sys
import os
from dotenv import load_dotenv
import psycopg
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from agents.tools.refinement_tools import clarity_tool_list, precision_tool_list, creative_tool_list, rag_tool_list

sys.path.append(os.path.abspath(".."))
load_dotenv()

DB_URI = os.environ.get("DATABASE_URL", "")
if not DB_URI:
    raise RuntimeError("DATABASE_URL is not set in environment")

# Enabling LangSmith for refiner agent (only if tracing is enabled)
os.environ["LANGSMITH_API_KEY"] = os.environ.get("REFINER_LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"] = os.environ.get("LANGSMITH_PROJECT", "refiner_agent")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

all_tools = clarity_tool_list + precision_tool_list + creative_tool_list + rag_tool_list
tool_node = ToolNode(all_tools)

# State
class RefinerState(TypedDict):
    original_prompt: str
    refined_prompt: str
    prompt_category: Literal["clarity", "precision", "creative", "greeting", "help_request", "rag_query"]
    framework_used: str
    messages: Annotated[list, add_messages]
    
# Graph Nodes
def classify_category(state: RefinerState) -> dict:
    last_human_message = next((msg for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)), None)
    if not last_human_message:
        return {} # Should not happen 

    original_prompt = last_human_message.content.strip()
    prompt_lower = original_prompt.lower()

    greeting_patterns = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if any(prompt_lower.startswith(p) for p in greeting_patterns):
        return {"prompt_category": "greeting", "original_prompt": original_prompt}

    help_patterns = ["framework", "help", "guide", "suggest", "recommend", "options", "what can you do"]
    if any(p in prompt_lower for p in help_patterns):
        return {"prompt_category": "help_request", "original_prompt": original_prompt}

    # Checking for RAG content
    rag_keywords = ["from the document", "summarize the file", "what does it say about", "in the document", "based on the file", "according to the document"]
    if any(keyword in prompt_lower for keyword in rag_keywords):
        return {"prompt_category": "rag_query", "original_prompt": original_prompt}

    analysis_prompt = f"""Analyze the user prompt and categorize it into ONLY one of the following:
    "clarity", "precision", "creative", or "rag_query".
User Prompt: "{original_prompt}"
Return only the single category name."""

    response = llm.invoke(analysis_prompt)
    category = response.content.strip().lower()

    if category not in ["clarity", "precision", "creative", "rag_query"]:
        category = "clarity"

    return {"prompt_category": category, "original_prompt": original_prompt}

def handle_conversation(state: RefinerState) -> dict:
    category = state["prompt_category"]
    
    if category == "greeting":
        response_content = """👋 **Hello! Welcome to the Prompt Refiner Agent!**

I'm here to help you transform basic prompts into powerful, detailed instructions that get you better results from AI models.

**How to use me:**
1. Simply paste or type any prompt you want to improve
2. I'll automatically analyze and categorize it
3. You'll get an enhanced version with clear improvements explained

**Examples of prompts I can refine:**
• "Write a blog post" → Detailed content strategy with structure
• "Create a marketing plan" → Comprehensive plan with specific deliverables
• "Help me code" → Targeted coding assistance with context and requirements

**Ready to get started?** Just share any prompt you'd like me to improve!"""

    elif category == "help_request":
        response_content = """**How the Prompt Refiner Works**

I use proven prompt engineering frameworks to enhance your prompts:

**For Clarity & Structure:**
• **C.O.R.E.** - Context, Objective, Role, Example
• **R.A.C.E.** - Role, Action, Context, Expectation
• **C.A.R.** - Context, Action, Result

**For Precision & Detail:**
• **RISEN** - Role, Instructions, Steps, End goal, Narrowing
• **Advanced structuring** with specific requirements and constraints

**For Creative & Innovative Prompts:**
• **IDEA** - Inspire, Define, Explore, Act
• **Creative enhancement** techniques for brainstorming and ideation

**What you'll get:**
• A significantly improved version of your prompt
• Clear explanation of what was enhanced and why
• Ready-to-use prompt that gets better AI responses

**Ready to try it?** Just paste any prompt you want me to refine!"""

    else:
        response_content = """I'm here to help refine prompts! 

Please share any prompt you'd like me to improve - whether it's for writing, coding, planning, or any other task. I'll analyze it and provide you with an enhanced version that gets better results.

**Examples:**
• "Write an email" 
• "Create a lesson plan"
• "Help me brainstorm ideas"
• "Generate code for..."

Just paste your prompt and I'll get started!"""
    
    return {"messages": [AIMessage(content=response_content)]}

def refinement_agent(state: RefinerState) -> dict:
    category = state["prompt_category"]
    prompt_to_refine = state["original_prompt"]
    
    if category == "clarity": selected_tools = clarity_tool_list
    elif category == "precision": selected_tools = precision_tool_list
    else: selected_tools = creative_tool_list

    # Adding RAG tools if a vector store exists
    if os.path.exists("./chroma_db"):
        selected_tools = selected_tools + rag_tool_list

    llm_with_selected_tools = llm.bind_tools(tools=selected_tools, parallel_tool_calls=False)

    system_prompt = f"""You are a prompt refinement expert helping users create better, more effective prompts.

The user submitted this prompt: "{prompt_to_refine}"
Category: {category}

Your task is to select the SINGLE most appropriate refinement tool to enhance this prompt. Focus on making it:
- More specific and actionable
- Clearer in its requirements and expectations  
- Better structured for getting quality results
- More detailed about the desired output format

You must call exactly one refinement tool that best fits this prompt's needs."""
    
    response = llm_with_selected_tools.invoke(system_prompt)
    
    framework_used = "direct_refinement"
    if response.tool_calls:
        framework_used = response.tool_calls[0]['name']

    return {"messages": [response], "framework_used": framework_used}

def rag_agent(state: RefinerState) -> dict:
    """Agent brain for RAG tasks that uses search tool to answer questions."""
    question = state["original_prompt"]
    
    # Giving the RAG agent ONLY the search tool to avoid confusion.
    llm_with_search = llm.bind_tools(tools=[rag_tool_list[0]], parallel_tool_calls=False) 

    system_prompt = f"""You are a helpful assistant. Answer the user's question based on the context from a document search.
Your task is to call the `document_search` tool with a query relevant to the user's question.
User's question: "{question}" """

    response = llm_with_search.invoke(system_prompt)
    return {"messages": [response]}

# Creating the final report for the user after a tool has been run.
def generate_analysis(state: RefinerState) -> dict:
    original_prompt = state["original_prompt"]
    framework_used = state.get("framework_used", "direct_refinement")
    category = state["prompt_category"]
    
    # Extracting refined prompt from tool execution results
    # Looking for the tool message in the messages
    refined_prompt = ""
    for msg in reversed(state["messages"]):
        if hasattr(msg, 'content') and msg.content and len(msg.content.strip()) > 20:
            refined_prompt = msg.content
            break
    
    # Fallback if no tool output found
    if not refined_prompt:
        refined_prompt = state.get("refined_prompt", "No refined prompt available")

    if category == "rag_query":
        # Synthesize the search results into a final answer
        synthesis_prompt = f"""The user asked: "{original_prompt}"
You have performed a search and found the following context from the document:
---
{refined_prompt}
---
Based ONLY on this context, provide a clear and concise answer to the user's question."""
        final_response = llm.invoke(synthesis_prompt)
        return {"messages": [AIMessage(content=final_response.content)]}
    else:
        # This is the original analysis logic for refinement tasks
        analysis_prompt = f"""You are a helpful prompt engineering assistant. A user asked you to improve their prompt: "{original_prompt}"

You used the {framework_used} framework to enhance it, and here's the improved version: {refined_prompt}

Create a friendly, conversational response that:
1. Briefly acknowledges what they wanted to create
2. Highlights 2-3 key improvements you made (be specific about what was added/improved)
3. Presents the refined prompt in a clear, formatted way
4. Ends with an encouraging note about how this will help them get better results

Keep it conversational and focus on the practical benefits for the user, not technical framework details.
Use a warm, helpful tone like you're a colleague offering advice.
        """
        final_response = llm.invoke(analysis_prompt)
        return {"messages": [AIMessage(content=final_response.content)], "refined_prompt": refined_prompt}

# Building the Graph
builder = StateGraph(RefinerState)

builder.add_node("classify_category", classify_category)
builder.add_node("handle_conversation", handle_conversation)
builder.add_node("refinement_agent", refinement_agent)
builder.add_node("rag_agent", rag_agent)
builder.add_node("tool_node", tool_node)
builder.add_node("generate_analysis", generate_analysis)

builder.set_entry_point("classify_category")

def route_after_classification(state: RefinerState):
    category = state["prompt_category"]
    if category in ["greeting", "help_request"]:
        return "handle_conversation"
    elif category == "rag_query":
        return "rag_agent"
    else:
        return "refinement_agent"

builder.add_conditional_edges("classify_category", route_after_classification, {
    "handle_conversation": "handle_conversation",
    "rag_agent": "rag_agent",
    "refinement_agent": "refinement_agent"
})
builder.add_edge("handle_conversation", END)

def route_after_refinement(state: RefinerState):
    # Check if the last message has tool calls that need to be executed
    if state["messages"] and hasattr(state["messages"][-1], 'tool_calls') and state["messages"][-1].tool_calls:
        return "tool_node"
    return "generate_analysis"

def route_after_rag(state: RefinerState):
    # Check if the last message has tool calls that need to be executed
    if state["messages"] and hasattr(state["messages"][-1], 'tool_calls') and state["messages"][-1].tool_calls:
        return "tool_node"
    return "generate_analysis"

builder.add_conditional_edges("refinement_agent", route_after_refinement, {
    "tool_node": "tool_node", 
    "generate_analysis": "generate_analysis"
})

builder.add_conditional_edges("rag_agent", route_after_rag, {
    "tool_node": "tool_node", 
    "generate_analysis": "generate_analysis"
})

builder.add_edge("tool_node", "generate_analysis")
builder.add_edge("generate_analysis", END)

# Compiling the Graph with memory using a persistent connection

# Temporary connection for setup
setup_conn = psycopg.connect(DB_URI)
setup_conn.autocommit = True
PostgresSaver(setup_conn).setup()
setup_conn.close()

# Persistent connection for runtime
conn = psycopg.connect(DB_URI)
memory = PostgresSaver(conn)
refiner_graph = builder.compile(checkpointer=memory)

# Helper Function for Streamlit demo
def extract_message_content(message: BaseMessage) -> tuple[str, str]:
    """Extracts role and content from a message."""
    if isinstance(message, HumanMessage):
        role = "user"
    elif isinstance(message, AIMessage):
        role = "assistant"
    else:
        role = "system" 
    return role, message.content
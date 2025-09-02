import sys
import os
from dotenv import load_dotenv
import psycopg
from typing import TypedDict, Annotated, List, Literal
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from agents.tools.refinement_tools import clarity_tool_list, precision_tool_list, creative_tool_list

sys.path.append(os.path.abspath(".."))

# Importing environment variables 
load_dotenv()

# Setting up PostgreSQL checkpointing
DB_URI = os.environ.get("DATABASE_URL", "")
if not DB_URI:
    raise RuntimeError("DATABASE_URL is not set in environment")

# Initializing llm
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

# Initializing PostgreSQL saver
saver = PostgresSaver.from_conn_string(DB_URI)

# Combining all tools
all_tools = clarity_tool_list + precision_tool_list + creative_tool_list 
llm_with_tools = llm.bind_tools(all_tools)
tool_node = ToolNode(all_tools)

# State of graph
class RefinerState(TypedDict):
    original_prompt: str
    refined_prompt: str
    prompt_category: Literal["clarity", "precision", "creative"]
    framework_used: str
    messages: Annotated[list, add_messages]

# Choosing which category users prompt falls 
def classify_category(state: RefinerState) -> dict:
    last_human_message = next((msg for msg in reversed(state["messages"])
        if isinstance(msg, HumanMessage)), None)

    if not last_human_message:
        return {"messages": [AIMessage(content="I couldn't find your prompt. Please provide it again.")]}

    prompt_to_analyze = last_human_message.content
    
    analysis_prompt = f"""
    Analyze the following user prompt and categorize it into ONLY one of the following: "clarity", "precision", or "creative".
    - "clarity": For prompts needing better structure or simpler language.
    - "precision": For prompts needing technical detail, constraints, or specific formatting.
    - "creative": For prompts needing brainstorming, imagination, or open-ended ideas.
    
    User Prompt: "{prompt_to_analyze}"
    
    Return only the single category name and nothing else.
    """
    
    response = llm.invoke(analysis_prompt)
    category = response.content.strip().lower()

    if category not in ["clarity", "precision", "creative"]:
        category = "clarity" # Default fallback incase failure to identify category

    print(f"Classified as: {category}")
    
    return {
        "original_prompt": prompt_to_analyze,
        "prompt_category": category
    }

# Selecting which framework under category to use
def refinement_agent(state: RefinerState) -> dict:
    category = state["prompt_category"]
    prompt_to_refine = state["original_prompt"]

    if category == "clarity":
        selected_tools = clarity_tool_list
    elif category == "precision":
        selected_tools = precision_tool_list
    else:
        selected_tools = creative_tool_list

    # Binding only the selected tools 
    llm_with_selected_tools = llm.with_tools(selected_tools)

    system_prompt = f"""
You are a prompt refinement expert. 
The user's prompt has been classified as '{category}'.
Your task is to select the SINGLE most appropriate refinement tool from your available tools to improve it.
You MUST call one and only one tool. Do not respond to the user directly.

User's prompt to refine: "{prompt_to_refine}"

Read the prompt carefully and refine it using the selected tool.
    """

    print(f"Invoking agent with {len(selected_tools)} tools for category '{category}' ")
    response = llm_with_selected_tools.invoke(system_prompt)
    
    return {"messages": [response]}

# analyzing prompt with the selected tool
def generate_analysis(state: RefinerState) -> dict:
    refined_prompt = state["messages"][-1].content
    
    tool_call = state["messages"][-2].tool_calls[0]
    framework_used = tool_call['name']
    
    category = state["prompt_category"]
    original_prompt = state["original_prompt"]

    analysis_prompt = f"""
You are an expert analyst. Create a final report for the user.
The user's prompt was classified under this '{category}'.
The '{framework_used}' framework was automatically chosen to refine it.

Explain in 1-2 sentences *why* '{framework_used}' was a good choice for this prompt.

**User's Original Prompt:**
"{original_prompt}"

**Refined Prompt:**
{refined_prompt}
    """
    
    final_response = llm.invoke(analysis_prompt)

    # Updating state 
    return {
        "refined_prompt": refined_prompt,
        "framework_used": framework_used,
        "messages": [AIMessage(content=final_response.content)]
    }
    
# Building the graph
builder = StateGraph(RefinerState)

# Adding nodes
builder.add_node("classify_category", classify_category)
builder.add_node("refinement_agent", refinement_agent)
builder.add_node('tool_node', tool_node)
builder.add_node("generate_analysis", generate_analysis)

# Starting point
builder.add_edge(START, "classify_category")

builder.add_edge("classify_category", "refinement_agent")

builder.add_conditional_edges(
    "refinement_agent",
    lambda x: "tool_node" if x["messages"][-1].tool_calls else END,
)

builder.add_edge("tool_node", "generate_analysis")
builder.add_edge("generate_analysis", END)

refiner_graph = builder.compile(checkpointer=saver)

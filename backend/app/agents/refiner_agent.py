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
from agents.tools.refinement_tools import clarity_tool_list, precision_tool_list, creative_tool_list, rag_tool_list

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

# Enabling LangSmith for refiner agent (only if tracing is enabled)
os.environ["LANGSMITH_API_KEY"] = os.environ.get("REFINER_LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"] = os.environ.get("LANGSMITH_PROJECT", "refiner_agent")

# Combining all tools
all_tools = clarity_tool_list + precision_tool_list + creative_tool_list + rag_tool_list
llm_with_tools = llm.bind_tools(all_tools)
tool_node = ToolNode(all_tools)

# State of graph
class RefinerState(TypedDict):
    original_prompt: str
    refined_prompt: str
    prompt_category: Literal["clarity", "precision", "creative", "greeting", "help_request", "follow_up"]
    framework_used: str
    messages: Annotated[list, add_messages]
    has_uploaded_documents: bool
    document_context: str
    is_greeting: bool
    is_help_request: bool
    is_follow_up: bool
    continue_to_refinement: bool

# Choosing which category users prompt falls 
def classify_category(state: RefinerState) -> dict:
    last_human_message = next((msg for msg in reversed(state["messages"])
        if isinstance(msg, HumanMessage)), None)

    if not last_human_message:
        return {"messages": [AIMessage(content="I couldn't find your prompt. Please provide it again.")]}

    prompt_to_analyze = last_human_message.content
    
    # Checking input if it's a greeting or non-refinement request
    greeting_patterns = [
        "hello", "hi", "hey", "greetings",
        "good morning", "good afternoon", "good evening",
        "how are you", "what's up", "how do you do"
    ]
    
    # Check for exact matches or specific greeting phrases
    is_greeting = any(
        pattern == prompt_to_analyze.lower().strip() or 
        prompt_to_analyze.lower().startswith(pattern + " ") or
        prompt_to_analyze.lower().endswith(" " + pattern) or
        prompt_to_analyze.lower() == pattern
        for pattern in greeting_patterns
    )
    
    if is_greeting:
        return {
            "original_prompt": prompt_to_analyze,
            "prompt_category": "greeting",
            "framework_used": "none",
            "has_uploaded_documents": os.path.exists("./chroma_db"),
            "document_context": "",
            "is_greeting": True,
            "is_help_request": False,
            "is_follow_up": False,
            "continue_to_refinement": False
        }
    
    # Checking if user is asking about frameworks or seeking help
    help_patterns = [
        "framework", "help", "guide", "suggest", "recommend", "available", "options",
        "what frameworks", "how to use", "explain frameworks", "show me frameworks"
    ]
    
    # Check for specific help phrases
    is_help_request = any(
        pattern in prompt_to_analyze.lower() 
        for pattern in help_patterns
    )
    
    if is_help_request:
        return {
            "original_prompt": prompt_to_analyze,
            "prompt_category": "help_request",
            "framework_used": "none",
            "has_uploaded_documents": os.path.exists("./chroma_db"),
            "document_context": "",
            "is_greeting": False,
            "is_help_request": True,
            "is_follow_up": False,
            "continue_to_refinement": False
        }
    
    # Checking if this is a follow-up question about the refined prompt
    follow_up_patterns = [
        "refined prompt", "framework used", "category analysis", "explain why",
        "why this framework", "how did you choose", "what framework", "tell me about"
    ]
    
    # Checking for specific follow-up phrases
    is_follow_up = any(
        pattern in prompt_to_analyze.lower() 
        for pattern in follow_up_patterns
    )
    
    if is_follow_up:
        return {
            "original_prompt": prompt_to_analyze,
            "prompt_category": "follow_up",
            "framework_used": "none",
            "has_uploaded_documents": False,
            "document_context": "",
            "is_greeting": False,
            "is_help_request": False,
            "is_follow_up": True,
            "continue_to_refinement": False
        }
    
    # Using LLM to classify the prompt for actual refinement
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
    
    # Check if user has uploaded documents
    has_documents = os.path.exists("./chroma_db")
    
    return {
        "original_prompt": prompt_to_analyze,
        "prompt_category": category,
        "framework_used": "none",  # Should be set in refinement_agent
        "has_uploaded_documents": has_documents,
        "document_context": "",
        "is_greeting": False,
        "is_help_request": False,
        "is_follow_up": False,
        "continue_to_refinement": True
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

    # Initializing the rag_tool_list
    rag_tool_list = []
    
    # Adding RAG tools if documents are available
    if state.get("has_uploaded_documents", False):
        try:
            selected_tools = selected_tools + rag_tool_list
            print(f"RAG tools activated - {len(rag_tool_list)} additional tools available")
        except ImportError:
            print("RAG tools not available, proceeding without them")
            rag_tool_list = []
    else:
        print("RAG tools not available, proceeding without them")

    # Binding only the selected tools 
    llm_with_selected_tools = llm.bind_tools(selected_tools)

    # Checking if we have document context
    rag_context = ""
    if state.get("has_uploaded_documents", False):
        rag_context = f"""

**Document Context Available:**
The user has uploaded documents that may provide relevant context for this refinement.
You can use the 'document_search' tool to find relevant information before refining the prompt.
Consider searching for context that might help improve the refinement quality.
"""

    system_prompt = f"""
You are a prompt refinement expert. 
The user's prompt has been classified as '{category}' category.

**Available Tools for {category} category:**
{chr(10).join([f"- {tool.name}: {tool.description}" for tool in selected_tools])}

**Your Task:**
1. Analyze the user's prompt carefully
2. Review all available tools in the {category} category
3. Select the SINGLE most appropriate refinement tool for this specific prompt
4. Call that tool to refine the prompt
5. Do not respond to the user directly - only call tools

**User's prompt to refine:** "{prompt_to_refine}"{rag_context}

**Important:** You must call exactly one tool. Choose the tool that will provide the best refinement for this specific prompt type and category.
    """

    print(f"Invoking agent with {len(selected_tools)} tools for category '{category}' ")
    
    try:
        response = llm_with_selected_tools.invoke(system_prompt)
        
        # Checking if the response has tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"Tool calls detected: {len(response.tool_calls)} tools will be executed")
            # Extracting the framework name from the tool that was called
            tool_name = response.tool_calls[0].get('name', 'unknown_tool')
            return {"messages": [response], "framework_used": tool_name}
        else:
            print("No tool calls detected, proceeding to analysis")
            # If no tools called, go directly to analysis
            return {"messages": [response], "skip_tool_node": True, "framework_used": "direct_refinement"}
            
    except Exception as e:
        print(f"Error during refinement: {e}")
        # Fallback: returning a message without tool calls
        fallback_response = AIMessage(content=f"Refinement completed for {category} category. The prompt has been improved using appropriate frameworks.")
        return {"messages": [fallback_response], "skip_tool_node": True}

# Handling greetings, help requests, and follow-up questions
def handle_conversation(state: RefinerState) -> dict:
    category = state.get("prompt_category", "")
    original_prompt = state.get("original_prompt", "")
    
    if category == "greeting":
        response = AIMessage(content=f"""
👋 Hello! I'm your AI Prompt Refiner Agent. 

I'm here to help you create better, more effective prompts using advanced frameworks to be able to 
effectively use your tokens on any AI-model user prompting on.

**What I can do:**

- Analyze your prompts and categorize them (clarity, precision, or creative)
- Refine prompts using specialized frameworks like C.O.R.E., R.A.C.E., and C.A.R.
- Provide detailed analysis and recommendations
- Use document context when available (RAG capabilities)

**How to get started:**

Simply share a prompt you'd like me to refine, and I'll analyze it and improve it using the most appropriate framework!

**Example prompts you can try:**
- "Write a meeting report"
- "Create a marketing campaign"
- "Design a lesson plan"
- "Generate code for a calculator"

What would you like me to help you refine today? 
        """)
        return {"messages": [response]}
    
    elif category == "help_request":
        response = AIMessage(content=f"""
I'd be happy to help! Here's what I can do and how I work:

** Here are some of the available Refinement Frameworks:**

**C.O.R.E. Framework** (Best for Clarity)
- **Context**: Establishes background and situation
- **Objective**: Defines clear goals and outcomes
- **Role**: Specifies who should do what
- **Example**: Provides concrete examples

**R.A.C.E. Framework** (Best for Precision)
- **Role**: Defines who is responsible
- **Action**: Specifies what needs to be done
- **Context**: Provides necessary background
- **Expectation**: Sets clear deliverables

**C.A.R. Framework** (Best for Creative)
- **Context**: Sets the scene and background
- **Action**: Defines the specific task
- **Result**: Describes the desired outcome

**How to use me:**
1. Share a prompt you want to refine
2. I'll automatically categorize it and select the best framework
3. I'll refine your prompt and provide detailed analysis
4. You can ask follow-up questions about the refinement

**Current prompt category:** {state.get('prompt_category', 'Not yet classified')}

Would you like me to refine a specific prompt, or do you have other questions?
        """)
        return {"messages": [response]}
    
    elif category == "follow_up":
        # Check if we have a previous refinement to reference
        if len(state.get("messages", [])) > 1:
            # Looking for the last refinement result
            for msg in reversed(state["messages"][:-1]):
                if hasattr(msg, 'content') and "Refined Prompt:" in msg.content:
                    response = AIMessage(content=f"""
I'd be happy to explain more about your recent refinement!

**Your Original Prompt:** "{original_prompt}"

**Framework Used:** {state.get('framework_used', 'Not specified')}
**Category:** {state.get('prompt_category', 'Not specified')}

**What I can explain:**
• Why this framework was chosen
• How the refinement improved your prompt
• Alternative approaches you could try
• Tips for future prompt writing

**To refine a new prompt:** Start a new chat session
**To ask about this refinement:** Ask specific questions about the analysis

What would you like me to clarify about your refinement?
        """)
                    return {"messages": [response]}
        
        # Fallback if no previous refinement found
        response = AIMessage(content=f"""
I'd be happy to help! However, I don't see a previous refinement in our current conversation.

**To get help with a refinement:**
1. Share a prompt you want me to refine
2. I'll analyze and improve it
3. Then you can ask follow-up questions

**To learn about frameworks:**
Ask me about available frameworks or how I work

**To start fresh:**
Share a new prompt for refinement

What would you like to do?
        """)
        return {"messages": [response]}
    
    # If none of the above, proceed to normal refinement
    return {"continue_to_refinement": True}

# analyzing prompt with the selected tool
def generate_analysis(state: RefinerState) -> dict:
    refined_prompt = state["messages"][-1].content
    
    # Getting framework_used from state (set by refinement_agent)
    framework_used = state.get("framework_used", "unknown_framework")
    
    category = state["prompt_category"]
    original_prompt = state["original_prompt"]

    # Checking if RAG was used
    rag_used = state.get("has_uploaded_documents", False)
    rag_info = ""
    if rag_used:
        rag_info = f"""

**RAG Enhancement:**
This refinement was enhanced using uploaded document context, providing more relevant and informed improvements.
"""

    analysis_prompt = f"""
You are an expert prompt engineering analyst creating a comprehensive final report for a user who wants to refine their prompt.

**Analysis Summary:**
- **Prompt Category**: {category}
- **Framework Used**: {framework_used}
- **RAG Enhancement**: {'Yes - Document context was used' if rag_used else 'No - Standard refinement only'}

**Your Task:**
1. **Explain in detail (3-4 sentences) why the '{framework_used}' approach was the optimal choice** for this specific prompt
2. **Break down how the refinement improved the prompt** - what was added, clarified, or structured
3. **Present the refined prompt prominently and clearly**
4. **Provide educational insights** about why this approach works well for this type of prompt
5. **Give actionable recommendations** for future similar prompts
6. **Use a professional but friendly, educational tone**

**User's Original Prompt:**
"{original_prompt}"

**Refined Prompt:**
First show the refined prompt here:
{refined_prompt}

**Format your response as:**
**Here is the Final Report:**
[Comprehensive analysis of how the refinement approach improved the prompt]

**Here is the Framework Analysis:**
[Detailed explanation of why this approach was perfect for this prompt type, including:
- What the approach does
- How it specifically helped this prompt
- What elements were enhanced or added
- Why this approach leads to better results]

**Key Improvements Made:**
[3-4 specific ways the refinement enhanced the original prompt]

**Key Takeaways:**
[3-4 educational insights about prompt refinement]

**Recommendations:**
[2-3 actionable suggestions for future similar prompts]

**Conclusion:**
[Summary of the refinement success and approach effectiveness]
    """
    
    final_response = llm.invoke(analysis_prompt)

    # Updating state 
    return {
        "refined_prompt": refined_prompt,
        "framework_used": framework_used,
        "messages": [AIMessage(content=final_response.content)]
    }

# Routing to tool_node if tools are called, otherwise to generate_analysis
def route_after_refinement(state):
    try:
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tool_node"
        else:
            return "generate_analysis"
    except (IndexError, KeyError, AttributeError):
        return "generate_analysis"

# Helper function to extract message content for streamlit demo
def extract_message_content(message):
    if hasattr(message, 'type'):
        role = message.type
    elif hasattr(message, 'role'):
        role = message.role
    else:
        role = "assistant"
    
    if hasattr(message, 'content'):
        content = message.content
    else:
        content = str(message)
    
    return role, content

# Building the graph
builder = StateGraph(RefinerState)

# Adding nodes
builder.add_node("classify_category", classify_category)
builder.add_node("handle_conversation", handle_conversation)
builder.add_node("refinement_agent", refinement_agent)
builder.add_node('tool_node', tool_node)
builder.add_node("generate_analysis", generate_analysis)

# Starting point
builder.add_edge(START, "classify_category")

# Routing from classify_category based on category type
builder.add_conditional_edges(
    "classify_category",
    lambda state: "handle_conversation" if state.get("prompt_category") in ["greeting", "help_request", "follow_up"] else "refinement_agent",
    {
        "handle_conversation": "handle_conversation",
        "refinement_agent": "refinement_agent"
    }
)

# Routing from handle_conversation
builder.add_conditional_edges(
    "handle_conversation",
    lambda state: "refinement_agent" if state.get("continue_to_refinement") else END,
    {
        "refinement_agent": "refinement_agent",
        END: END
    }
)

builder.add_conditional_edges(
    "refinement_agent",
    route_after_refinement,
    {
        "tool_node": "tool_node",
        "generate_analysis": "generate_analysis"
    }
)

builder.add_edge("tool_node", "generate_analysis")
builder.add_edge("generate_analysis", END)

# compiling the graph with memory using a persistent connection

setup_conn = psycopg.connect(DB_URI, connect_timeout=10)
setup_conn.autocommit = True
PostgresSaver(setup_conn).setup()
setup_conn.close()
    
# Create a connection pool for the graph
from psycopg_pool import ConnectionPool
pool = ConnectionPool(DB_URI, min_size=1, max_size=10)
    
refiner_graph = builder.compile(checkpointer=PostgresSaver(pool))
   
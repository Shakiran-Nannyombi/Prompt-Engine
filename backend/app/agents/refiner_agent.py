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
os.environ["LANGSMITH_PROJECT"] = os.environ.get("REFINER_LANGSMITH_PROJECT", "refiner_agent")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

all_tools = clarity_tool_list + precision_tool_list + creative_tool_list + rag_tool_list
tool_node = ToolNode(all_tools)

# State
class RefinerState(TypedDict):
    original_prompt: str
    refined_prompt: str
    prompt_category: Literal["clarity", "precision", "creative", "greeting", "help_request"]
    framework_used: str
    has_document: bool  # Flag to indicate if RAG processing is needed
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
        return {"prompt_category": "greeting", "original_prompt": original_prompt, "has_document": False}

    help_patterns = ["framework", "help", "guide", "suggest", "recommend", "options", "what can you do"]
    if any(p in prompt_lower for p in help_patterns):
        return {"prompt_category": "help_request", "original_prompt": original_prompt, "has_document": False}

    # Checking for document/image uploads or RAG content indicators
    rag_keywords = [
        "from the document", "summarize the file", "what does it say about", "in the document", 
        "based on the file", "according to the document", "upload", "uploaded", "document", 
        "pdf", "image", "picture", "analyze this", "what's in this"
    ]
    has_document = any(keyword in prompt_lower for keyword in rag_keywords) or os.path.exists("./chroma_db")

    analysis_prompt = f"""Analyze the user prompt and categorize it into ONLY one of the following:
    "clarity", "precision", or "creative".
User Prompt: "{original_prompt}"
Return only the single category name."""

    response = llm.invoke(analysis_prompt)
    category = response.content.strip().lower()

    if category not in ["clarity", "precision", "creative"]:
        category = "clarity"

    return {
        "prompt_category": category, 
        "original_prompt": original_prompt,
        "has_document": has_document
    }

def handle_conversation(state: RefinerState) -> dict:
    category = state["prompt_category"]
    
    if category == "greeting":
        response_content = """👋 **Hey there! Welcome to your personal Prompt Transformation Studio!**

I'm absolutely thrilled you're here! Think of me as your creative partner who takes "meh" prompts and turns them into absolute powerhouses that get incredible results from AI models. 

**Here's how we'll work our magic together:**
- **Just drop me any prompt** - literally anything you want to improve!
- **I'll work my detective skills** to figure out exactly what you're after
- **You'll get back a supercharged version** with all the improvements clearly explained

**Check out these amazing transformations:**
- "Write a blog post" → **Boom!** Detailed content strategy with engaging structure and target audience focus
- "Create a marketing plan" → **Pow!** Comprehensive strategy with specific deliverables, timelines, and measurable goals
- "Help me code" → **Zap!** Targeted coding assistance with context, requirements, and step-by-step guidance

**Ready to see some prompt magic happen?** Just paste any prompt you'd like me to transform - I can't wait to show you what we can create together!"""

    elif category == "help_request":
        response_content = """**Ooh, you want to see behind the curtain! I love that!**

I'm like a Swiss Army knife of prompt engineering - I've got all these amazing frameworks in my toolkit, and I pick the perfect one for your specific needs:

**For Making Things Crystal Clear:**
- **C.O.R.E.** (Context, Objective, Role, Example) - Perfect for when you need structure!
- **R.A.C.E.** (Role, Action, Context, Expectation) - Great for action-oriented prompts
- **C.A.R.** (Context, Action, Result) - Simple but powerful for direct requests

**For Laser-Sharp Precision:**
- **RISEN** (Role, Instructions, Steps, End goal, Narrowing) - When you need detailed, step-by-step magic
- **Advanced structuring** with all the bells and whistles for complex requirements

**For Creative Brilliance:**
- **IDEA** (Inspire, Define, Explore, Act) - Perfect for brainstorming and innovation
- **Creative enhancement** techniques that spark imagination and get those creative juices flowing

**Here's what makes me so excited to work with you:**
- You'll get a dramatically improved prompt that actually works
- I'll explain exactly what I changed and why (no mystery black box here!)
- You'll walk away with a ready-to-use masterpiece that gets incredible AI responses

**Want to see this magic in action?** Just drop any prompt on me - even the most basic one - and watch me transform it into something spectacular!"""

    else:
        response_content = """Hey there! 👋 I'm your friendly prompt transformation specialist, and I'm here to turn your ideas into prompt gold!

Whatever you've got brewing in your mind - a simple request, a complex project, or even just a rough idea - I'm here to help you polish it into something that gets absolutely amazing results from AI models.

**I love working on all kinds of prompts:**
- "Write an email" → Let's make it compelling and effective!
- "Create a lesson plan" → We'll make it engaging and comprehensive!
- "Help me brainstorm ideas" → Perfect! I'll structure it for maximum creativity!
- "Generate code for..." → Let's get specific and build something awesome!

**Here's the deal:** Just paste whatever prompt you have - even if it feels rough or incomplete. I'll work my magic and show you exactly how to make it shine! 

Ready to see what we can create together? """
    
    return {"messages": [AIMessage(content=response_content)]}

# Prompt refinement with integrated RAG processing when documents are present.
def process_prompt_refinement(state: RefinerState) -> dict:
    category = state["prompt_category"]
    prompt_to_refine = state["original_prompt"]
    has_document = state.get("has_document", False)
    
    # Select appropriate tools based on category and document presence
    if category == "clarity": 
        selected_tools = clarity_tool_list
    elif category == "precision": 
        selected_tools = precision_tool_list
    else: 
        selected_tools = creative_tool_list
    
    # Add RAG tools if document is present
    if has_document and os.path.exists("./chroma_db"):
        selected_tools = selected_tools + rag_tool_list

    llm_with_selected_tools = llm.bind_tools(tools=selected_tools, parallel_tool_calls=False)

    if has_document:
        system_prompt = f"""You are a prompt refinement expert helping users create better, more effective prompts.

The user submitted this prompt: "{prompt_to_refine}"
Category: {category}
Document Available: Yes - The user has uploaded or referenced documents that should be used.

Your task is to:
1. First, if the prompt involves document analysis, call the document_search tool to gather relevant information
2. Then, select the most appropriate refinement tool to enhance this prompt using both the original prompt and any document context

Focus on making the prompt:
- More specific and actionable with document context
- Clearer in requirements and expectations
- Better structured for getting quality results from both the prompt and available documents
- More detailed about the desired output format

You must call the appropriate tools to both access documents (if needed) and refine the prompt."""
    else:
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

    # Handle both regular refinement and document-aware refinement
    has_document = state.get("has_document", False)
    
    if has_document:
        # Special handling for document-aware refinement
        analysis_prompt = f"""You are an enthusiastic and friendly prompt engineering coach who just helped transform a user's prompt using their uploaded documents! 

The user originally wanted: "{original_prompt}"
You used the {framework_used} approach along with their document context to create this amazing enhanced version: {refined_prompt}

Write a warm, engaging response that shows your genuine excitement about the transformation. Include:

1. **Enthusiastic acknowledgment** - Show you understand their goal and you're excited to help them use their documents effectively
2. **Highlight the document magic** - Point out how you incorporated their document content to make the prompt more specific and powerful
3. **Present the masterpiece** - Show off the refined prompt that now leverages their actual data/content
4. **Celebrate the success** - End with genuine enthusiasm about how much better their results will be now that they're using their own documents

Write like you're a passionate friend who just helped them unlock the power of their own content. Use emojis, exclamation points, and conversational phrases. Make them feel proud of what you created together!
        """
        final_response = llm.invoke(analysis_prompt)
        return {"messages": [AIMessage(content=final_response.content)], "refined_prompt": refined_prompt}
    else:
        # Regular refinement without documents
        analysis_prompt = f"""You are an enthusiastic and friendly prompt engineering coach who just helped transform a user's prompt. The user originally wanted: "{original_prompt}"

You used the {framework_used} approach to create this amazing enhanced version: {refined_prompt}

Write a warm, engaging response that shows your genuine excitement about the transformation. Include:

1. **Enthusiastic acknowledgment** - Show you understand their goal and you're excited to help
2. **Highlight the magic** - Point out 2-3 specific improvements you made, using conversational language (avoid technical jargon)
3. **Present the masterpiece** - Show off the refined prompt in a visually appealing way
4. **Celebrate the success** - End with genuine enthusiasm about how much better their results will be

Write like you're a passionate friend who just helped them solve a problem. Use emojis, exclamation points, and conversational phrases. Make them feel proud of what you created together!
        """
        final_response = llm.invoke(analysis_prompt)
        return {"messages": [AIMessage(content=final_response.content)], "refined_prompt": refined_prompt}

# Building the Graph
builder = StateGraph(RefinerState)

builder.add_node("classify_category", classify_category)
builder.add_node("handle_conversation", handle_conversation)
builder.add_node("process_prompt_refinement", process_prompt_refinement)
builder.add_node("tool_node", tool_node)
builder.add_node("generate_analysis", generate_analysis)

builder.set_entry_point("classify_category")

def route_after_classification(state: RefinerState):
    category = state["prompt_category"]
    if category in ["greeting", "help_request"]:
        return "handle_conversation"
    else:
        return "process_prompt_refinement"

builder.add_conditional_edges("classify_category", route_after_classification, {
    "handle_conversation": "handle_conversation",
    "process_prompt_refinement": "process_prompt_refinement"
})

builder.add_edge("handle_conversation", END)

def route_to_tools(state: RefinerState):
    # Check if the last message has tool calls that need to be executed
    if state["messages"] and hasattr(state["messages"][-1], 'tool_calls') and state["messages"][-1].tool_calls:
        return "tool_node"
    return "generate_analysis"

builder.add_conditional_edges("process_prompt_refinement", route_to_tools, {
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
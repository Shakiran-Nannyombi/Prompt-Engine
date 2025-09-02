import sys
import os
import language_tool_python
from dotenv import load_dotenv
import psycopg
from typing import TypedDict, Annotated, List
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from backend.app.agents.tools import coach_tools
from models.grammarResult import GrammarResult

sys.path.append(os.path.abspath(".."))

# Importing environment variables from .env
load_dotenv()

# Setup PostgreSQL checkpointing
DB_URI = os.environ.get("DATABASE_URL", "")
if not DB_URI:
    raise RuntimeError("DATABASE_URL is not set in environment")


# State of grammar correction graph
class GrammarState(TypedDict):
    original_text: str
    corrected_text: str
    corrections_made: List[str]
    suggestions: List[str]
    messages: Annotated[list, add_messages]
    current_step: str
    grammar_result: GrammarResult

# Models
llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0.3
)

tool_node = ToolNode([coach_tools.check_grammar])
llm_with_grammar = llm.with_structured_output(GrammarResult)
llm_with_tools = llm.bind_tools(tools=[coach_tools.check_grammar], parallel_tool_calls=False)

instruction = ("""
You are an expert English grammar assistant. Your task is to help users improve their
writing by identifying and correcting grammar, spelling, punctuation, and clarity issues in their text.
You will correct their text and provide the corrected version as the new output for the agent it
will be working with.
You work with both the coach agent and refuner agent to provide comprehensive grammar assistance to user inputs.
When correcting text, focus on the following:
1. Grammar: Ensure subject-verb agreement, correct tense usage, proper article usage, and
   correct prepositions.
2. Spelling: Identify and correct any misspelled words.
3. Punctuation: Ensure proper use of commas, periods, semicolons, colons, quotation marks, and other punctuation marks.
4. Clarity: Suggest improvements to sentence structure for better readability and flow.
When providing corrections, always include a brief explanation of the changes made and
suggest any additional improvements that could enhance the overall quality of the text.""")

def start_grammar_correction(state: GrammarState):
    existing_messages = state.get("messages", [])
    if existing_messages:
        return {"current_step": state.get("current_step", "awaiting_text")}
    return {
        "messages": [SystemMessage(content=instruction)],
        "current_step": "awaiting_text"
    }

def process_text_input(state: GrammarState):
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"current_step": "error"}
    
    last_message = messages[-1]
    user_text = last_message.content.strip()
    
    if not user_text:
        return {
            "messages": [AIMessage(content="Please provide some text for me to correct.")],
            "current_step": "awaiting_text"
        }
    
    # Storing original text
    state["original_text"] = user_text
    
    try:
        # Using directly for immediate grammar correction
        tool = language_tool_python.LanguageTool('en-UK')
        matches = tool.check(user_text)
        corrected_text = language_tool_python.utils.correct(user_text, matches)

        
    except Exception as e:
        error_message = f""" **Error during grammar correction:** {str(e)}
Please try again with your text, or let me know if you need help with a specific grammar issue.
        """
        return {
            "messages": [AIMessage(content=error_message)],
            "current_step": "awaiting_text"
        }

 # Routing to the appropriate next step based on user input
def decide_next_step(state: GrammarState):
    messages = state.get("messages", [])
    if not messages:
        return "start_grammar_correction"
    
    last_message = messages[-1]
    if not isinstance(last_message, HumanMessage):
        return END
    
    user_input = last_message.content.lower().strip()
    
    # Check for greetings
    if user_input in ["hi", "hello", "hey", "sup", "yo"] or len(user_input) < 5:
        return "handle_greeting"
    
    # Process text for grammar correction
    return "process_text_input"

# Build the graph
builder = StateGraph(GrammarState)

# Add nodes
builder.add_node("start_grammar_correction", start_grammar_correction)
builder.add_node("process_text_input", process_text_input)

# Add edges
builder.add_edge(START, "start_grammar_correction")
builder.add_conditional_edges(
    "start_grammar_correction",
    decide_next_step,
    {
        "process_text_input": "process_text_input",
        END: END
    }
)

# Compile the graph
# Temporary connection for setup
setup_conn = psycopg.connect(DB_URI)
setup_conn.autocommit = True
PostgresSaver(setup_conn).setup()
setup_conn.close()

# Persistent connection for runtime
conn = psycopg.connect(DB_URI)
memory = PostgresSaver(conn)
grammar_graph = builder.compile(checkpointer=memory)

# Helper function to extract message content
def extract_message_content(messages):
    """Extract content from LangChain messages for API response"""
    extracted_messages = []
    for message in messages:
        if hasattr(message, 'content'):
            extracted_messages.append({
                "role": message.__class__.__name__.lower().replace('message', ''),
                "content": message.content
            })
    return extracted_messages

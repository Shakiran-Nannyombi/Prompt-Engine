from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
import language_tool_python
from dotenv import load_dotenv

# Load environment variables first (project root if present)
load_dotenv()

tavily_search = TavilySearch(max_results=3)

class GrammarCheckArgs(BaseModel):
    text: str = Field(
        description="The text to be checked for grammar and spelling."
        )

@tool("grammar_checker", args_schema=GrammarCheckArgs, return_direct=False)
def check_grammar(text: str) -> str:
    """
    Checks the provided text for grammar and spelling errors and returns a corrected version.
    Use this to polish and refine a final prompt or any user-provided text.
    """
    try:
        tool = language_tool_python.LanguageTool('en-UK')
        matches = tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        return f"Grammar check complete. Here is the corrected text:\n---\n{corrected_text}"
    except Exception as e:
        return f"Error during grammar check: {e}"

@tool
def tavily_search_tool(query: str) -> str:
    """
    Use this tool to search the web for relevant information using Tavily.
    Input should be a search query.
    """
    try:
        results = tavily_search.run(query)
        if not results:
            return "No results found."
        formatted_results = "\n".join([f"- {res['title']}: {res['link']}" for res in results])
        return f"Search results:\n{formatted_results}"
    except Exception as e:
        return f"Error during Tavily search: {e}"

tool_list = [tavily_search_tool, check_grammar]
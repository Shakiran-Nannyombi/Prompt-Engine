from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import language_tool_python
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

tavily_search = TavilySearch(max_results=3)


# @tool("grammar_checker", args_schema=GrammarResult, return_direct=False)
# def check_grammar(original_text: str) -> GrammarResult:
#     """
#     Checks the provided text for grammar and spelling errors and returns a structured result.
#     Use this to analyze and correct grammar issues in user text.
#     """
#     try:
#         tool = language_tool_python.LanguageTool('en-UK')
#         matches = tool.check(original_text)
#         corrected_text = language_tool_python.utils.correct(original_text, matches)
#         return GrammarResult(
#             original_text=original_text,
#             corrected_text=corrected_text,
#             corrections_made=[match.message for match in matches],
#             suggestions=[]
#         )
#     except Exception as e:
#         return f"Error during grammar check: {e}"

@tool
def tavily_search_tool(query: str) -> str:
    """
    Use this tool to search the web for relevant information using Tavily.
    Input should be a search query.
    """
    # Perform a web search using Tavily and return formatted results
    try:
        results = tavily_search.run(query)
        if not results:
            return "No results found."
        formatted_results = "\n".join([f"- {res['title']}: {res['link']}" for res in results])
        return f"Search results:\n{formatted_results}"
    except Exception as e:
        return f"Error during Tavily search: {e}"

tool_list = [tavily_search_tool]
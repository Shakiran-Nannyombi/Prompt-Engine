from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

# Web search tool
tavily_search_tool = TavilySearchResults(max_results=3)

tool_list = [tavily_search_tool]
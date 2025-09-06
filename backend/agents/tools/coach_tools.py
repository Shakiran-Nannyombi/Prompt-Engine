from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

# Web search tool
tavily_search_tool = TavilySearch(max_results=3)

tool_list = [tavily_search_tool]
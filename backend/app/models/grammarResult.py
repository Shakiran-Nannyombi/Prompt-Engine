import language_tool_python
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import List


# Grammar correction result 
class GrammarResult(BaseModel):
    original_text: str = Field(description="The original text provided by the user")
    corrected_text: str = Field(description="The grammar-corrected version of the text")
    corrections_made: List[str] = Field(description="List of specific corrections made")
    suggestions: List[str] = Field(description="Additional suggestions for improvement")


    

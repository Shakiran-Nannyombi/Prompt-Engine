from pydantic import BaseModel

# Data model for the final analysis provided to the user.
class RefinementAnalysis(BaseModel):
    category: str
    framework_used: str
    reasoning: str
    refined_prompt: str
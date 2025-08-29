from pydantic import BaseModel
from typing  import List

# model for api response to frontend
class CoachingResponse(BaseModel):
    agent_output:str
    refined_prompt: str = None
    conversation_history: List[dict]
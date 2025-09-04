from pydantic import BaseModel
from typing import List

# Model for API response to frontend
class CoachingResponse(BaseModel):
    agent_output: str
    refined_prompt: List[str] = None
    conversation_history: List[dict]
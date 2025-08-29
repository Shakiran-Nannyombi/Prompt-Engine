from pydantic import BaseModel
from typing import List

# Model for API request from the frontend
class CoachingRequest(BaseModel):
    user_input: str
    conversation_history: List[dict] = None 

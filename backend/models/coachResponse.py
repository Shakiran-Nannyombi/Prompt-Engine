from pydantic import BaseModel
from typing import List, Optional

# Model for API response to frontend
class CoachingResponse(BaseModel):
    agent_output: str
    refined_prompt: Optional[str] = None
    conversation_history: List[dict]
from pydantic import BaseModel
from typing import List, Optional

# Model for API request from the frontend
class CoachingRequest(BaseModel):
    user_input: str
    conversation_history: Optional[List[dict]] = None
    thread_id: Optional[str] = None  # For conversation thread management

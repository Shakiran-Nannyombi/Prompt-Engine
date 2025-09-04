from pydantic import BaseModel
from typing import Optional, List

# Model for refiner api request from the frontend
class RefinerRequest(BaseModel):
    original_prompt: str
    conversation_history: Optional[List[dict]] = None
    thread_id: Optional[str] = None  # for conversation thread management
    has_document: Optional[bool] = False  # for rag processing

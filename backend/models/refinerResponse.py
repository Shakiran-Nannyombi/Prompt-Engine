from pydantic import BaseModel
from typing import List, Optional
from app.models.refine_prompt import RefinementAnalysis

# Model for refiner api response to frontend
class RefinerResponse(BaseModel):
    agent_output: str
    refined_prompt: Optional[str] = None
    prompt_category: Optional[str] = None
    framework_used: Optional[str] = None
    refinement_analysis: Optional[RefinementAnalysis] = None
    conversation_history: List[dict]

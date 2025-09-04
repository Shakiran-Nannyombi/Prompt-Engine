from pydantic import BaseModel, Field
from typing import Optional

class EvaluationResult(BaseModel):
    is_correct: bool = Field(
        description="""
        True if the user input is acceptable as a valid task, context, reference, or final prompt.
        Be LENIENT - accept inputs that show clear intent even if they need refinement.
        Only set to False for completely invalid, harmful, or nonsensical inputs.
        """
    )
    
    feedback: str = Field(
        description="""
        Provide constructive, encouraging feedback.
        - If is_correct=True: Give positive reinforcement and maybe suggest enhancements
        - If is_correct=False: Explain what's needed and provide helpful examples
        Always be supportive and guide the user toward success.
        """
    )
    
    updated_prompt: Optional[str] = Field(
        default=None,
        description="""
        An improved version of the user's input (optional).
        Only provide if you have a clear, better alternative.
        Most of the time, leave this as None and let the user refine their own input.
        """
    )
    
    suggestions: Optional[list[str]] = Field(
        default=None,
        description="List of specific suggestions for improvement. Optional field."
    )
    
        
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional

class EvaluationResult(BaseModel):
    # Pydantic v2 config (replaces deprecated class Config)
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "examples": [
                {
                    "is_correct": True,
                    "feedback": "Great task! This is clear and actionable. To make it even better, you could specify the target audience or specific features you want.",
                    "updated_prompt": None,
                    "suggestions": [
                        "Consider specifying the target grade level",
                        "Think about specific subject areas to focus on",
                    ],
                },
                {
                    "is_correct": False,
                    "feedback": "I need a bit more information to help you. Could you tell me what specific task you'd like to accomplish? For example: 'Write a blog post', 'Create a chatbot', or 'Generate code for an app'.",
                    "updated_prompt": None,
                    "suggestions": [
                        "Provide a specific goal or outcome",
                        "Describe what you want to create or accomplish",
                    ],
                },
            ]
        },
    )
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
    
    # (No class Config; using model_config above)
        
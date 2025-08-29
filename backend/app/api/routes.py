from fastapi import APIRouter
from app.api import prompt_coach

api_router = APIRouter()

api_router.include_router(prompt_coach.router, prefix="/coaching", tags=["coaching"])

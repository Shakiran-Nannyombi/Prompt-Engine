from fastapi import APIRouter
from fastApi import prompt_coach, prompt_refiner

api_router = APIRouter()

api_router.include_router(prompt_coach.router, prefix="/coaching", tags=["coaching"])
api_router.include_router(prompt_refiner.router, prefix="/refiner", tags=["refiner"])

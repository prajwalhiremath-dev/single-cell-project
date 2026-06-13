from fastapi import APIRouter

from app.api.v1.datasets import router as datasets_router
from app.api.v1.experiments import router as experiments_router

api_router = APIRouter()
api_router.include_router(datasets_router)
api_router.include_router(experiments_router)

from fastapi import APIRouter
from src.presentation.api.v1.user.router import user_router
from src.presentation.api.v1.auth.router import auth_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(user_router)
api_v1_router.include_router(auth_router)
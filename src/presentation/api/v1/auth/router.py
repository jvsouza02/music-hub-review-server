from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from .schema import TokenResponseSchema
from src.application.auth.services import AuthService
from src.presentation.api.v1.auth.deps import get_auth_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login", response_model=TokenResponseSchema)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> TokenResponseSchema:
    token: str = await auth_service.authenticate_user(
        form_data.username, form_data.password
    )
    return TokenResponseSchema(access_token=token)
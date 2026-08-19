from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from typing import Annotated
from .schema import LoginResponseSchema
from src.application.auth.services import AuthService
from src.presentation.api.v1.auth.deps import get_auth_service
from .cookies import (set_access_cookie, refresh_access_cookie,
clear_auth_cookie)
from src.core.security import decode_token
from .constants import REFRESH_TOKEN_KEY

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login", response_model=LoginResponseSchema)
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> LoginResponseSchema:
    access_token, refresh_token, _ = await auth_service.authenticate_user(
        form_data.username, form_data.password
    )

    set_access_cookie(response, access_token)
    refresh_access_cookie(response, refresh_token)

    return LoginResponseSchema(
        access_token=access_token,
        message="User successfully logged!"
    )

    
@auth_router.post("/refresh", response_model=LoginResponseSchema)
async def refresh(
    request: Request,
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service)
    ]
) -> LoginResponseSchema:
    refresh_token = request.cookies.get(REFRESH_TOKEN_KEY) 

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )
    
    (
    new_access_token, 
    new_refresh_access_token,
    _
    ) = await auth_service.refresh_access_token(refresh_token)

    set_access_cookie(response, new_access_token)
    refresh_access_cookie(response, new_refresh_access_token)

    return LoginResponseSchema(
        access_token=new_refresh_access_token,
        message="Token was successfully refreshed"
    )


@auth_router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service)
    ]
) -> dict[str, str]:
    refresh_token = request.cookies.get(REFRESH_TOKEN_KEY)
    refresh_jti = None

    if refresh_token:
        try:
            payload = decode_token(refresh_token)
            refresh_jti  = payload.get("jti")
        except Exception:
            pass

    await auth_service.logout(refresh_jti)
    clear_auth_cookie(response)
    
    return {"message": "User succesfully logged out"}
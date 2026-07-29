from fastapi import APIRouter, status, Depends, Body, Path
from typing import Annotated
from uuid import UUID
from src.application.user.services import UserService
from src.domain.user.entity import User
from src.presentation.api.v1.auth.deps import get_current_user
from .schema import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from .deps import get_user_service


user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/", response_model=list[UserResponseSchema])
async def get_users(
     user_service: Annotated[UserService, Depends(get_user_service)]
) -> list[UserResponseSchema]:
     return await user_service.get_users()

@user_router.get("/me", response_model=UserResponseSchema)
async def get_me(
     current_user: Annotated[User, Depends(get_current_user)]
) -> UserResponseSchema:
     return current_user


@user_router.get("/{user_id}")
async def get_user():
     pass


@user_router.post(
     "/",
     response_model=UserResponseSchema,
     status_code=status.HTTP_201_CREATED  
)
async def create_user(
     data: Annotated[UserCreateSchema, Body()],
     user_service: Annotated[
          UserService,
          Depends(get_user_service)
     ]
) -> UserResponseSchema:
     return await user_service.create_user(**data.model_dump())


@user_router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(
     user_id: Annotated[UUID, Path()],
     data: Annotated[UserUpdateSchema, Body()],
     user_service: Annotated[UserService, Depends(get_user_service)]
):
     return await user_service.edit_user(user_id, **data.model_dump())


@user_router.patch("/{user_id}")
async def partial_update_user():
     pass


@user_router.delete("/{user_id}")
async def delete_user():
     pass

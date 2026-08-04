from fastapi import APIRouter, status, Depends, Body, Path
from typing import Annotated
from uuid import UUID
from src.application.user.services import UserService
from src.domain.user.entity import User
from src.presentation.api.v1.auth.deps import (get_current_user,
get_moderator_admin_user, get_authorized_user)
from .schema import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from .deps import get_user_service


user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get(
          "/",
          response_model=list[UserResponseSchema],
          status_code=status.HTTP_200_OK,
          dependencies=[Depends(get_moderator_admin_user)]
)
async def get_users(
     user_service: Annotated[UserService, Depends(get_user_service)]
) -> list[UserResponseSchema]:
     return await user_service.get_users()

@user_router.get(
          "/me",
          response_model=UserResponseSchema,
          status_code=status.HTTP_200_OK
)
async def get_me(
     current_user: Annotated[User, Depends(get_current_user)]
) -> UserResponseSchema:
     return current_user


@user_router.get(
          "/{user_id}",
          response_model=UserResponseSchema,
          status_code=status.HTTP_200_OK,
)
async def get_user(
     user_id: Annotated[UUID, Path()],
     user_service: Annotated[UserService, Depends(get_user_service)],
     _=Depends(get_authorized_user)
):
     return await user_service.get_user(user_id)


@user_router.post(
          "/",
          response_model=UserResponseSchema,
          status_code=status.HTTP_201_CREATED  
)
async def create_user(
     data: Annotated[UserCreateSchema, Body()],
     user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponseSchema:
     return await user_service.create_user(**data.model_dump())


@user_router.patch(
          "/{user_id}",
          response_model=UserResponseSchema,
          status_code=status.HTTP_200_OK,
          dependencies=[Depends(get_authorized_user)]
)
async def update_user(
     user_id: Annotated[UUID, Path()],
     data: Annotated[UserUpdateSchema, Body()],
     user_service: Annotated[UserService, Depends(get_user_service)]
):
     return await user_service.edit_user(
          user_id,
          **data.model_dump(exclude_unset=True)
     )


@user_router.delete(
          "/{user_id}",
          status_code=status.HTTP_204_NO_CONTENT,
          dependencies=[Depends(get_authorized_user)]
)
async def delete_user(
     user_id: Annotated[UUID, Path()],
     user_service: Annotated[UserService, Depends(get_user_service)]
):
     await user_service.delete_user(user_id)

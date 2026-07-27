from fastapi import APIRouter, status, Depends
from typing import Annotated
from src.application.user.services import UserService
from src.domain.user.entity import User
from src.presentation.api.v1.auth.deps import get_current_user
from .schema import UserCreateSchema, UserResponseSchema
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
     data: UserCreateSchema,
     user_service: Annotated[
          UserService,
          Depends(get_user_service)
     ]
) -> UserResponseSchema:
     created_user = await user_service.create_user(**data.model_dump())
     return created_user


@user_router.put("/{user_id}")
async def update_user():
     pass


@user_router.patch("/{user_id}")
async def partial_update_user():
     pass


@user_router.delete("/{user_id}")
async def delete_user():
     pass

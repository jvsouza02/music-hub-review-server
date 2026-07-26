from fastapi import APIRouter, status, Depends
from typing import Annotated
from src.application.user.services import UserService
from .schema import UserCreateSchema, UserResponseSchema
from .deps import get_user_service

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/")
async def get_users():
     pass


@user_router.get("/me")
async def get_me():
     pass


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

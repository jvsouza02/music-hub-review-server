from fastapi import APIRouter

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


@user_router.post("/")
async def create_user():
     pass


@user_router.put("/{user_id}")
async def update_user():
     pass


@user_router.patch("/{user_id}")
async def partial_update_user():
     pass


@user_router.delete("/{user_id}")
async def delete_user():
     pass

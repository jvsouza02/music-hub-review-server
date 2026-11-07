from fastapi import APIRouter
from src.presentation.api.v1.user.router import user_router
from src.presentation.api.v1.auth.router import auth_router
from src.presentation.api.v1.review.router import review_router
from src.presentation.api.v1.artist.router import artist_router
from src.presentation.api.v1.album.router import album_router
from src.presentation.api.v1.track.router import track_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(user_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(review_router)
api_v1_router.include_router(artist_router)
api_v1_router.include_router(album_router)
api_v1_router.include_router(track_router)
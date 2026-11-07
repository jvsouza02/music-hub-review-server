from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.presentation.api.v1.router import api_v1_router
from src.domain.global_exception import GlobalException
from src.core.config import settings
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from src.infrastructure.cache.redis_client import RedisClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = RedisClient().client
    await FastAPILimiter.init(redis)
    yield
    await FastAPILimiter.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)


@app.exception_handler(GlobalException)
async def global_exception_handler(
    request: Request,
    exception: GlobalException
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.message}
    )


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "message": "Music Hub Review Server is running!"
    }
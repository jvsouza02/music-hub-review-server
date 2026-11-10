from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.presentation.api.v1.router import api_v1_router
from src.domain.global_exception import GlobalException
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Accept",
        "Authorization",
        "Content-Type",
        "X-CSRF-Token",
        "X-Request-ID",
    ],
    expose_headers=[
        "Retry-After",
        "X-Request-ID",
    ],
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
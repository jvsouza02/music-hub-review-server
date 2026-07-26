from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.presentation.api.v1.router import api_v1_router
from src.domain.global_exception import GlobalException

app = FastAPI()

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
        "version": "1.0.0",
        "message": "Music Hub Review Server is running!"
    }
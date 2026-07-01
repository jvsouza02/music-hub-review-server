from fastapi import FastAPI
from presentation.api.v1.router import api_v1_router

app = FastAPI()

app.include_router(api_v1_router)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "Music Hub Review Server is running!"
    }
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from app.web.user_info import router as user_info_router
from app.service.user_info import start_location_updates, stop_location_updates


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute on startup: start location update service
    start_location_updates()
    yield
    # Execute on shutdown: stop location update service
    stop_location_updates()


app = FastAPI(
    title="Elder Care MVP",
    version="0.1.0",
    lifespan=lifespan
)
app.include_router(user_info_router)

@app.get("/")
async def root():
    return {"message": "Hello from elder-care-mvp!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

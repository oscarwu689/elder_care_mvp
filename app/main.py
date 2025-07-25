from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, WebSocket
from app.web.user_info_v1 import router as user_info_v1_router
from app.web.user_info_v2 import router as user_info_v2_router
from app.service.user_info import start_location_updates, stop_location_updates
from fastapi.responses import HTMLResponse
from app.scripts.html_script import html

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
app.include_router(user_info_v1_router)
app.include_router(user_info_v2_router)



@app.get("/")
async def root():
    return HTMLResponse(content=html, status_code=200)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# websocket endpoint for chat test
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

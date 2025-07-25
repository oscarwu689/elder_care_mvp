from fastapi import FastAPI
from app.web.user_info import router as user_info_router
from app.service.user_info import start_location_updates

app = FastAPI(title="Elder Care MVP", version="0.1.0")
app.include_router(user_info_router)

@app.get("/")
async def root():
    return {"message": "Hello from elder-care-mvp!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """應用程式啟動時自動開始位置更新"""
    start_location_updates()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

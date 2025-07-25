from fastapi import FastAPI
from app.web.user_info import router as user_info_router

app = FastAPI(title="Elder Care MVP", version="0.1.0")
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

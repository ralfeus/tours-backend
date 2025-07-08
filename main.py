from fastapi import FastAPI
from routers import users, requests, tours, feedbacks, auth

app = FastAPI(title="Tours Management API", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/user", tags=["users"])
app.include_router(requests.router, prefix="/request", tags=["requests"])
app.include_router(tours.router, prefix="/tour", tags=["tours"])
app.include_router(feedbacks.router, prefix="/feedback", tags=["feedbacks"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Tours Management API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

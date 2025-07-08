from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import users, requests, tours, feedbacks, auth
import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="Tours Management API", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/user", tags=["users"])
app.include_router(requests.router, prefix="/request", tags=["requests"])
app.include_router(tours.router, prefix="/tour", tags=["tours"])
app.include_router(feedbacks.router, prefix="/feedback", tags=["feedbacks"])

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content={
#             "detail": exc.errors(),
#             "body": exc.body,
#             "message": "Validation error occurred"
#         },
#     )

origins = [
    "*",  # your frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # allow these origins
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # allow all headers
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Tours Management API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from app.routes import users
import uvicorn


app = FastAPI(title="PaymentApp Server")

app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
from fastapi import FastAPI
from pymongo import MongoClient
from app.routes.metrics import metrics_router
from app.routes.candidate import candidate_router
from contextlib import asynccontextmanager
import uvicorn
from app.auth_users.app import app as auth_users_app

app = FastAPI()

# Include the metrics router
app.include_router(metrics_router)
app.include_router(candidate_router)

# MongoDB connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient("mongodb://localhost:27017")
    app.database = app.mongodb_client["menstrual_db"]  # Replace with your database name
    print("Connected to MongoDB!")
    yield
    app.mongodb_client.close()
    print("Disconnected from MongoDB!")

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")
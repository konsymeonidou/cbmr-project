from fastapi import FastAPI
from pymongo import MongoClient
from app.routes.metrics import metrics_router
from app.routes.candidate import candidate_router
from contextlib import asynccontextmanager

app = FastAPI()

# Include the metrics router
app.include_router(metrics_router)
app.include_router(candidate_router)

# MongoDB connection
# @app.on_event("startup")
# def startup_db_client():
#     app.mongodb_client = MongoClient("mongodb://localhost:27017")
#     app.database = app.mongodb_client["menstrual_db"]  # Replace with your database name
#     print("Connected to MongoDB!")

# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()
#     print("Disconnected from MongoDB!")
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient("mongodb://localhost:27017")
    app.database = app.mongodb_client["menstrual_db"]  # Replace with your database name
    print("Connected to MongoDB!")
    yield
    app.mongodb_client.close()
    print("Disconnected from MongoDB!")

app.router.lifespan_context = lifespan
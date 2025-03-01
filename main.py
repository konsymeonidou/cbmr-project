from fastapi import FastAPI, Depends
from pymongo import MongoClient
from app.routes.metrics import metrics_router
from app.routes.candidate import candidate_router
from contextlib import asynccontextmanager
import uvicorn

from app.auth_users.db import User
from app.auth_users.schemas import UserCreate, UserRead, UserUpdate
from app.auth_users.users import auth_backend, current_active_user, fastapi_users

app = FastAPI()


# MongoDB connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient("mongodb://localhost:27017")
    app.database = app.mongodb_client["menstrual_db"]  # Replace with your database name
    app.database = app.mongodb_client["users_db"]
    print("Connected to MongoDB!")
    yield
    app.mongodb_client.close()
    print("Disconnected from MongoDB!")


app.router.lifespan_context = lifespan

# Include the metrics router
app.include_router(metrics_router)
app.include_router(candidate_router)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")

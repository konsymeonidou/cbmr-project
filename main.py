from fastapi import FastAPI
from app.routes.metrics import metrics_router
from app.routes.candidate import candidate_router

app = FastAPI()

# Include the metrics router
app.include_router(metrics_router)
app.include_router(candidate_router)

# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Health Metrics API!"}
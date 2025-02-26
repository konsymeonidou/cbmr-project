from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.models.metrics import HealthMetrics
from bson import ObjectId


def get_collection_metrics(request: Request):
  return request.app.database["metrics"]

def create_HealthMetrics(request: Request, HealthMetrics: HealthMetrics = Body(...)):
    healthmetrics = jsonable_encoder(HealthMetrics)
    new_HealthMetrics = get_collection_metrics(request).insert_one(healthmetrics)
    created_HealthMetrics = get_collection_metrics(request).find_one({"_id": new_HealthMetrics.inserted_id})
    return created_HealthMetrics


def list_HealthMetrics(request: Request, limit: int):
    healthmetrics = list(get_collection_metrics(request).find(limit = limit))
    for healthmetric in healthmetrics:
        healthmetric["_id"] = str(healthmetric["_id"])
    return healthmetrics


def find_HealthMetrics(request: Request, id: str):
    if (healthmetrics := get_collection_metrics(request).find_one({"_id": ObjectId(id)})):
        healthmetrics["_id"] = str(healthmetrics["_id"])
        return healthmetrics
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"HealthMetrics with id {id} not found!")


def delete_HealthMetrics(request: Request, id: str):
    deleted_HealthMetrics = get_collection_metrics(request).delete_one({"_id": ObjectId(id)})

    if deleted_HealthMetrics.deleted_count == 1:
        return f"HealthMetrics with id {id} deleted sucessfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"HealthMetrics with id {id} not found!")
from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.models.metrics import HealthMetrics
from bson import ObjectId


def get_collection_metrics(request: Request):
  return request.app.database["metrics"]

def create_HealthMetrics(request: Request, HealthMetrics: HealthMetrics = Body(...)):
    HealthMetrics = jsonable_encoder(HealthMetrics)
    new_HealthMetrics = get_collection_metrics(request).insert_one(HealthMetrics)
    created_HealthMetrics = get_collection_metrics(request).find_one({"_id": new_HealthMetrics.inserted_id})
    if created_HealthMetrics:
        created_HealthMetrics["id"] = created_HealthMetrics["_id"]
    return created_HealthMetrics


def list_HealthMetrics(request: Request, limit: int):
    HealthMetrics = list(get_collection_metrics(request).find(limit = limit))
    return HealthMetrics


def find_HealthMetrics(request: Request, id: str):
    if (HealthMetrics := get_collection_metrics(request).find_one({"health_id": ObjectId(id)})):
        return HealthMetrics
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"HealthMetrics with id {id} not found!")


def delete_HealthMetrics(request: Request, id: str):
    deleted_HealthMetrics = get_collection_metrics(request).delete_one({"health_id": ObjectId(id)})

    if deleted_HealthMetrics.deleted_count == 1:
        return f"HealthMetrics with health_id {id} deleted sucessfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"HealthMetrics with health_id {id} not found!")
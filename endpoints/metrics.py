from fastapi import APIRouter, Request, status
from typing import List
from models import HealthMetrics
from rules import Metrics



router = APIRouter(prefix="/metrics",
    tags=["Metrics"])

@router.post("/", response_description="Create health metrics", status_code=status.HTTP_201_CREATED, response_model=HealthMetrics)
def create_metrics(request: Request, metrics: HealthMetrics):
    return Metrics.create_metrics(request, metrics)


@router.put("/{health_id}", response_description="Update health metrics", response_model=HealthMetrics)
def update_metrics(request: Request, id: str, metrics: HealthMetrics):
    return Metrics.update_metrics(request, id, metrics)

@router.get("/", response_description="List all Metrics", response_model=List[HealthMetrics])
def list_Metrics(request: Request):
    return Metrics.list_Metrics(request, 100)


@router.get("/{candidate_id}/", response_description="List Metrics by candidate id", response_model=HealthMetrics)
def list_Metrics_by_id(request: Request, candidate_id: str):
    return Metrics.list_Metrics_by_id(request, candidate_id)


@router.delete("/{health_id}", response_description="Delete health metrics")
def delete_metrics(request: Request, id: str):
    return Metrics.delete_metrics(request, id)
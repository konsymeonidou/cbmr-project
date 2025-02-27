from fastapi import APIRouter, Request, status, HTTPException, Query
from app.models.metrics import HealthMetrics, HealthMetricsResponse
from app.rules.metrics import (
    create_HealthMetrics,
    list_HealthMetrics,
    find_HealthMetrics,
    delete_HealthMetrics,
)
from typing import List, Optional

metrics_router = APIRouter(prefix="/metrics", tags=["metrics"])


@metrics_router.post(
    "/",
    response_description="Create health metrics",
    status_code=status.HTTP_201_CREATED,
    response_model=HealthMetrics,
)
def create_metrics(request: Request, metrics: HealthMetrics):
    try:
        return create_HealthMetrics(request, metrics)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@metrics_router.get(
    "/",
    response_description="List all Metrics",
    response_model=List[HealthMetricsResponse],
)
def list_Metrics(
    request: Request,
    limit: Optional[int] = Query(100, description="Limit the number of results"),
):
    try:
        return list_HealthMetrics(request, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@metrics_router.get(
    "/{id}",
    response_description="Get Metrics by health ID",
    response_model=HealthMetricsResponse,
)
def get_Metrics_by_id(request: Request, health_id: str):
    try:
        return find_HealthMetrics(request, health_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@metrics_router.delete("/{id}", response_description="Delete health metrics")
def delete_metrics(request: Request, health_id: str):
    try:
        return delete_HealthMetrics(request, health_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

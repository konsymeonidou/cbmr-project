from fastapi import APIRouter, Request, status
from models.metrics import HealthMetrics
from rules.metrics import create_HealthMetrics

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/", response_description="Create health metrics", status_code=status.HTTP_201_CREATED, response_model=HealthMetrics)
def create_metrics(request: Request, metrics: HealthMetrics):
    return create_HealthMetrics(request, metrics)

# @router.put("/{health_id}", response_description="Update health metrics", response_model=HealthMetrics)
# def update_metrics(request: Request, id: str, metrics: HealthMetrics):
#     return metrics.update_metrics(request, id, metrics)

# @router.get("/", response_description="List all Metrics", response_model=List[HealthMetrics])
# def list_Metrics(request: Request):
#     return metrics.list_Metrics(request, 100)

# @router.get("/{candidate_id}/", response_description="List Metrics by candidate id", response_model=HealthMetrics)
# def list_Metrics_by_id(request: Request, candidate_id: str):
#     return metrics.list_Metrics_by_id(request, candidate_id)

# @router.delete("/{health_id}", response_description="Delete health metrics")
# def delete_metrics(request: Request, id: str):
#     return metrics.delete_metrics(request, id)
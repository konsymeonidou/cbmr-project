from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import uuid


class CycleMetrics(BaseModel):
    flow: int
    mood: str
    steps: int
    weight: float
    high_days: int

    class Config:
        schema_extra = {
            "example": {
                "flow": 3,
                "mood": "Happy",
                "steps": 10000,
                "weight": 72.5,
                "high_days": 3
            }
        }

class OptionalMetrics(BaseModel):
    # Optional fields
    height: Optional[float]
    blood_type: Optional[str]
    allergies: Optional[str]
    medications: Optional[str]
    conditions: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "height": 1.75,
                "blood_type": "A+",
                "allergies": "Pollen",
                "medications": "Ibuprofen",
                "conditions": "Asthma"
            }
        }

class HealthMetrics(BaseModel):
    health_id: str = Field(default_factory=uuid.uuid4, alias="id")
    candidate_id: str
    date: date
    daily_metrics: CycleMetrics
    optional_metrics: Optional[OptionalMetrics]
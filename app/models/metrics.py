from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import date
from bson import ObjectId


class CycleMetrics(BaseModel):
    flow: int
    mood: str
    steps: int
    weight: float
    high_days: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "flow": 3,
                "mood": "Happy",
                "steps": 10000,
                "weight": 72.5,
                "high_days": 3,
            }
        }
    )

    @field_validator("flow")
    def validate_flow(cls, v):
        if v < 0:
            raise ValueError("Flow must be a positive integer")
        return v

    @field_validator("weight")
    def validate_weight(cls, v):
        if v <= 0:
            raise ValueError("Weight must be greater than 0")
        return v


class OptionalMetrics(BaseModel):
    # Optional fields
    height: Optional[float]
    blood_type: Optional[str]
    allergies: Optional[str]
    medications: Optional[str]
    conditions: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "height": 1.75,
                "blood_type": "A+",
                "allergies": "Pollen",
                "medications": "Ibuprofen",
                "conditions": "Asthma",
            }
        }
    )


class HealthMetrics(BaseModel):
    candidate_id: str
    date: date
    daily_metrics: CycleMetrics
    optional_metrics: Optional[OptionalMetrics]

    model_config = ConfigDict(populate_by_name=True)


# Model used for output (GET)
class HealthMetricsResponse(HealthMetrics):
    id: Optional[str] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

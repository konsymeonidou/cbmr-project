from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Candidate(BaseModel):
    name: str
    email: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    age: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Mary Doe",
                "email": "[email protected]",
                "phone_number": "555-555-5555",
                "address": "123 Main Street, Springfield, IL",
                "age": 30,
            }
        },
        populate_by_name=True,
    )


# Model used for output (GET)
class CandidateResponse(Candidate):
    id: Optional[str] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

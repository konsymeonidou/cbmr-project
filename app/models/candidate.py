from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class Candidate(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    email: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    age: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mary Doe",
                "email": "[email protected]",
                "phone_number": "555-555-5555",
                "address": "123 Main Street, Springfield, IL",
                "age": 30
            }
        }
        populate_by_name = True 
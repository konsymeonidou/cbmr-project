from pydantic import BaseModel, Field
from typing import Optional
import uuid

class Candidate(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    name: str
    email: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    age: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Mary Doe",
                "email": "[email protected]",
                "phone_number": "555-555-5555",
                "address": "123 Main Street, Springfield, IL",
                "age": 30
            }
        }
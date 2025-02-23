from fastapi import APIRouter, Body, Request, status
from typing import List
from models import Candidate
import rules as Candidates


router = APIRouter(prefix="/Candidate",
    tags=["Candidate"])

@router.post("/", response_description="Create a new Candidate", status_code=status.HTTP_201_CREATED, response_model=Candidate)
def create_Candidate(request: Request, Candidate: Candidate = Body(...)):  
    return Candidates.create_Candidate(request,Candidate)

@router.get("/", response_description="List Candidates", response_model=List[Candidate])
def list_Candidates(request: Request):
    return Candidates.list_Candidates(request, 100)

@router.get("/{id}", response_description="Get a single Candidate by id", response_model=Candidate)
def find_Candidate(request: Request, id: str):    
    return Candidates.find_Candidate(request, id)


@router.delete("/{id}", response_description="Delete a Candidate")
def delete_Candidate(request: Request, id:str):
    return Candidates.delete_Candidate(request, id)
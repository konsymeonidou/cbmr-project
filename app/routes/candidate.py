from fastapi import APIRouter, Body, Request, status, HTTPException
from typing import List
from app.models.candidate import Candidate, CandidateResponse
from app.rules.candidate import (
    create_candidate,
    list_candidates,
    find_candidate,
    delete_candidate,
)

candidate_router = APIRouter(prefix="/candidates", tags=["candidates"])

@candidate_router.post("/", response_description="Create a new candidate", status_code=status.HTTP_201_CREATED, response_model=Candidate)
def create_candidate_route(request: Request, candidate: Candidate = Body(...)):
    try:
        return create_candidate(request, candidate)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@candidate_router.get("/", response_description="List candidates", response_model=List[CandidateResponse])
def list_candidates_route(request: Request, limit: int = 100):
    try:
        return list_candidates(request, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@candidate_router.get("/{id}", response_description="Get a single candidate by id", response_model=CandidateResponse)
def find_candidate_route(request: Request, id: str):
    try:
        return find_candidate(request, id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@candidate_router.delete("/{id}", response_description="Delete a candidate")
def delete_candidate_route(request: Request, id: str):
    try:
        return delete_candidate(request, id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
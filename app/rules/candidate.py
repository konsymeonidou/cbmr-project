from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Candidate
from bson import ObjectId


def get_collection_Candidate(request: Request):
  return request.app.database["Candidates"]

def create_Candidate(request: Request, Candidate: Candidate = Body(...)):
    Candidate = jsonable_encoder(Candidate)
    new_Candidate = get_collection_Candidate(request).insert_one(Candidate)
    created_Candidate = get_collection_Candidate(request).find_one({"id": new_Candidate.inserted_id})
    return created_Candidate


def list_Candidates(request: Request, limit: int):
    Candidates = list(get_collection_Candidate(request).find(limit = limit))
    return Candidates


def find_Candidate(request: Request, id: str):
    if (Candidate := get_collection_Candidate(request).find_one({"id": ObjectId(id)})):
        return Candidate
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with id {id} not found!")


def delete_Candidate(request: Request, id: str):
    deleted_Candidate = get_collection_Candidate(request).delete_one({"_id": ObjectId(id)})

    if deleted_Candidate.deleted_count == 1:
        return f"Candidate with id {id} deleted sucessfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with id {id} not found!")
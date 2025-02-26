from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.models.candidate import Candidate
from bson import ObjectId


def get_collection_candidate(request: Request):
    return request.app.database["candidates"]


def create_candidate(request: Request, candidate: Candidate = Body(...)):
    candidate = jsonable_encoder(candidate)
    new_candidate = get_collection_candidate(request).insert_one(candidate)
    created_candidate = get_collection_candidate(request).find_one({"_id": new_candidate.inserted_id})
    if created_candidate:
        created_candidate["id"] = created_candidate["_id"]
    return created_candidate


def list_candidates(request: Request, limit: int):
    candidates = list(get_collection_candidate(request).find().limit(limit))
    return candidates


def find_candidate(request: Request, id: str):
    if (candidate := get_collection_candidate(request).find_one({"_id": id})):
        return candidate
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with id {id} not found!")


def delete_candidate(request: Request, id: str):
    deleted_candidate = get_collection_candidate(request).delete_one({"_id": id})

    if deleted_candidate.deleted_count == 1:
        return f"Candidate with id {id} deleted successfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with id {id} not found!")
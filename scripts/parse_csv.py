import csv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["menstrual_db"]


def insert_candidate(db, candidate_data):
    """Insert candidate and return its ObjectId"""
    result = db["candidates"].insert_one(candidate_data)
    return str(result.inserted_id)


def parse_csv_and_insert(file_path):
    """Parse a combined CSV and insert records into MongoDB"""
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract candidate data
            candidate_data = {
                "name": row["name"],
                "email": row["email"],
                "phone_number": row["phone_number"],
                "address": row["address"],
                "age": int(row["age"]),
            }

            # Extract cycle metrics
            cycle_metrics = {
                "flow": int(row["flow"]),
                "mood": row["mood"],
                "steps": int(row["steps"]),
                "weight": float(row["weight"]),
                "high_days": int(row["high_days"]),
            }

            # Extract optional metrics
            optional_metrics = {
                "height": float(row["height"]) if row["height"] else None,
                "blood_type": row["blood_type"] if row["blood_type"] else None,
                "allergies": row["allergies"] if row["allergies"] else None,
                "medications": row["medications"] if row["medications"] else None,
                "conditions": row["conditions"] if row["conditions"] else None,
            }

            # Construct and insert health metrics
            health_metrics = {
                "candidate_id": insert_candidate(db, candidate_data),
                "date": row["date"],
                "daily_metrics": cycle_metrics,
                "optional_metrics": optional_metrics,
            }
            db["metrics"].insert_one(health_metrics)


# Example Usage
parse_csv_and_insert("./sample_data/data.csv")

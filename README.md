# prediction-pipeline
This is the formative assignment of building an ML pipeline.
"""
MongoDB Schema Documentation:

1. Plants Collection:
{
    "_id": ObjectId,
    "name": string (unique, required),
    "created_at": datetime
}

2. Diseases Collection:
{
    "_id": ObjectId,
    "name": string (unique, required),
    "created_at": datetime
}

3. Images Collection:
{
    "_id": ObjectId,
    "filename": string (required),
    "path": string (required),
    "plant_id": ObjectId (reference to Plants),
    "disease_id": ObjectId (reference to Diseases),
    "split": string ("train" or "val"),
    "created_at": datetime
}
"""
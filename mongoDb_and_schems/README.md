# Plant Disease Prediction Pipeline

## Overview
This repository contains an ML pipeline for plant disease prediction with a MongoDB backend. The database schema follows strict validation rules defined in JSON Schema files.

## Database Schema Documentation

### Collections Structure

#### 1. Plants Collection
Stores information about plant species.

**Schema Definition:** [plants.json](./mongoDb_and_schemas/schema-plant_disease_dataset-plants-standardJSON.json)

```json
{
  "_id": { "$oid": "5f8d3a7d4b1c2e3d4c5e6f7b" },
  "name": "Tomato",
  "created_at": { "$date": "2023-05-15T10:00:00Z" }
}
```

**Fields:**
- `_id`: Unique identifier (ObjectId)
- `name`: Plant name (unique, required)
- `created_at`: Timestamp of record creation (ISO date)

---

#### 2. Diseases Collection
Stores information about plant diseases.

**Schema Definition:** [diseases.json](./mongoDb_and_schemas/schema-plant_disease_dataset-diseases-standardJSON.json)

```json
{
  "_id": { "$oid": "5f8d3a7d4b1c2e3d4c5e6f7c" },
  "name": "Bacterial spot",
  "created_at": { "$date": "2023-05-15T10:00:00Z" }
}
```

**Fields:**
- `_id`: Unique identifier (ObjectId)
- `name`: Disease name (unique, required)
- `created_at`: Timestamp of record creation (ISO date)

---

#### 3. Images Collection
Stores image metadata and relationships.

**Schema Definition:** [images.json](./mongoDb_and_schemas/schema-plant_disease_dataset-images-standardJSON.json)

```json
{
  "_id": { "$oid": "5f8d3a7d4b1c2e3d4c5e6f7a" },
  "filename": "Tomato_Bacterial_spot_001.jpg",
  "path": "/data/PlantVillage/train/Tomato___Bacterial_spot/Tomato_Bacterial_spot_001.jpg",
  "plant_id": { "$oid": "5f8d3a7d4b1c2e3d4c5e6f7b" },
  "disease_id": { "$oid": "5f8d3a7d4b1c2e3d4c5e6f7c" },
  "split": "train",
  "created_at": { "$date": "2023-05-15T10:05:23Z" }
}
```

**Fields:**
- `_id`: Unique identifier (ObjectId)
- `filename`: Original image filename
- `path`: Absolute path to image file
- `plant_id`: Reference to Plants collection (ObjectId)
- `disease_id`: Reference to Diseases collection (ObjectId)
- `split`: Dataset split ("train" or "val")
- `created_at`: Timestamp of record creation (ISO date)

## Schema Validation
All collections enforce strict validation through JSON Schema definitions:

1. **Required Fields**: All documents must contain specified required fields
2. **Data Types**: Enforces correct data types and formats
3. **ObjectId Validation**: Ensures valid 24-character hex strings
4. **Date Validation**: Requires ISO 8601 date format

## Relationships
- Each image references exactly one plant via `plant_id`
- Each image references exactly one disease via `disease_id`
- Plants and diseases can be referenced by multiple images

## Indexes
1. `Plants.name`: Unique index
2. `Diseases.name`: Unique index
3. `Images.path`: Unique index

## Schema Files
- [Plants Collection Schema](./mongoDb_and_schemas/schema-plant_disease_dataset-plants-standardJSON.json)
- [Diseases Collection Schema](./mongoDb_and_schemas/schema-plant_disease_dataset-diseases-standardJSON.json)
- [Images Collection Schema](./mongoDb_and_schemas/schema-plant_disease_dataset-images-standardJSON.json)
```
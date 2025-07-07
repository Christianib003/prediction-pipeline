#!/usr/bin/env python3

import os
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint


# ATLAS_CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/plant_disease_dataset?retryWrites=true&w=majority"
ATLAS_CONNECTION_STRING = ATLAS_CONNECTION_STRING = "mongodb+srv://lchristian:o6wrlRSowzEDEJky@cluster0.cqxlda3.mongodb.net/plant_disease_dataset?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "plant_disease_dataset"

# Dataset configuration
DATASET_DIR = "data/PlantVillage"
MAX_IMAGES_PER_CATEGORY = 10000  # 

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

def get_mongo_client():
    """Create and return MongoDB Atlas client"""
    try:
        client = MongoClient(ATLAS_CONNECTION_STRING)
        # Test the connection
        client.admin.command('ping')
        print(" Successfully connected to MongoDB Atlas")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas: {e}")
        raise

def initialize_database(client):
    """Initialize database with proper indexes"""
    db = client[DATABASE_NAME]
    
    # Create collections if they don't exist
    plants = db.plants
    diseases = db.diseases
    images = db.images
    
    # Create indexes
    plants.create_index("name", unique=True)
    diseases.create_index("name", unique=True)
    images.create_index([("path", 1)], unique=True)
    
    print(" Database initialized with proper indexes")
    return db

def parse_category_name(category):
    """Parse category name into plant and disease"""
    if "___" in category:
        parts = category.split("___")
        plant = parts[0].replace("(maize)", "maize").strip()
        disease = parts[1].replace("_", " ").strip()
        return plant, disease
    return category.replace("(maize)", "maize").strip(), "healthy"

def process_dataset(db):
    """Process the dataset and insert into MongoDB"""
    plants = db.plants
    diseases = db.diseases
    images = db.images
    
    categories = [
        "Corn_(maize)___Common_rust_",
        "Corn_(maize)___healthy",
        "Potato___Early_blight",
        "Potato___healthy",
        "Tomato___Bacterial_spot",
        "Tomato___healthy"
    ]
    
    for split in ["val"]:
        split_dir = os.path.join(DATASET_DIR, split)
        if not os.path.exists(split_dir):
            print(f" {split} directory not found. Skipping.")
            continue
            
        for category in categories:
            category_path = os.path.join(split_dir, category)
            if not os.path.exists(category_path):
                print(f" {category} not found in {split}. Skipping.")
                continue
                
            plant_name, disease_name = parse_category_name(category)
            
            # Get or create plant
            plant = plants.find_one({"name": plant_name})
            if not plant:
                plant_id = plants.insert_one({
                    "name": plant_name,
                    "created_at": datetime.now()
                }).inserted_id
            else:
                plant_id = plant["_id"]
            
            # Get or create disease
            disease = diseases.find_one({"name": disease_name})
            if not disease:
                disease_id = diseases.insert_one({
                    "name": disease_name,
                    "created_at": datetime.now()
                }).inserted_id
            else:
                disease_id = disease["_id"]
            
            # Process images
            image_count = 0
            for img_file in os.listdir(category_path):
                if image_count >= MAX_IMAGES_PER_CATEGORY:
                    break
                    
                img_path = os.path.join(category_path, img_file)
                if not os.path.isfile(img_path):
                    continue
                    
                # Check if image already exists
                existing = images.find_one({"path": os.path.relpath(img_path, start=DATASET_DIR)})
                if existing:
                    continue
                    
                # Insert image metadata
                images.insert_one({
                    "filename": img_file,
                    "path": os.path.relpath(img_path, start=DATASET_DIR),
                    "plant_id": plant_id,
                    "disease_id": disease_id,
                    "split": split,
                    "created_at": datetime.now()
                })
                image_count += 1
                
            print(f" Processed {image_count} images from {split}/{category}")

def main():
    try:
        # Connect to MongoDB Atlas
        client = get_mongo_client()
        db = initialize_database(client)
        
        # Process and insert dataset
        process_dataset(db)
        
        # Print some stats
        print("\n Database Stats:")
        print(f"- Plants: {db.plants.count_documents({})}")
        print(f"- Diseases: {db.diseases.count_documents({})}")
        print(f"- Images: {db.images.count_documents({})}")
        
    except Exception as e:
        print(f" An error occurred: {e}")
    finally:
        if 'client' in locals():
            client.close()
            print(" MongoDB connection closed")

if __name__ == "__main__":
    main()
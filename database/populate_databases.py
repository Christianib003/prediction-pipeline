import os
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Configuration
load_dotenv()
POSTGRES_URL = os.getenv("DATABASE_URL")
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
DATASET_DIR = "data/PlantVillage/test"


def populate_databases():
    """Connects to both databases and populates them with data."""
    pg_conn = None
    mongo_client = None
    
    try:
        # Connect to both databases
        print("Connecting to PostgreSQL...")
        pg_conn = psycopg2.connect(POSTGRES_URL)
        pg_cursor = pg_conn.cursor()
        print("Connecting to MongoDB...")
        mongo_client = MongoClient(MONGO_URL)
        mongo_db = mongo_client[MONGO_DB_NAME]
        images_collection = mongo_db.images
        print("Connections successful.")

        # Process dataset and populate ---
        if not os.path.exists(DATASET_DIR):
            print(f"Error: Dataset directory not found at '{DATASET_DIR}'")
            return

        for folder_name in os.listdir(DATASET_DIR):
            folder_path = os.path.join(DATASET_DIR, folder_name)
            if not os.path.isdir(folder_path):
                continue
            
            try:
                plant_name, disease_name = folder_name.split('___')
                disease_name = disease_name.replace('_', ' ')
            except ValueError:
                continue

            print(f"\nProcessing folder: {folder_name}")
            
            # Limit the number of images per category to 10
            image_count = 0
            for filename in os.listdir(folder_path):
                if image_count >= 10:
                    print("  - Reached limit of 10 images for this category.")
                    break

                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(folder_path, filename).replace("\\", "/")

                    pg_cursor.execute("CALL add_new_image(%s, %s, %s, %s)", (filename, image_path, plant_name, disease_name))
                    pg_conn.commit()
                    
                    pg_cursor.execute("SELECT image_id, date_added FROM image_metadata WHERE image_path = %s", (image_path,))
                    sql_result = pg_cursor.fetchone()
                    
                    if not sql_result:
                        print(f"  - Could not retrieve ID for '{filename}'.")
                        continue
                    
                    sql_image_id, date_added = sql_result
                    
                    mongo_doc = {
                        "sql_image_id": sql_image_id,
                        "filename": filename,
                        "image_path": image_path,
                        "plant": {"name": plant_name},
                        "disease": {"name": disease_name},
                        "date_added": date_added,
                        "predictions": []
                    }
                    images_collection.insert_one(mongo_doc)
                    print(f"  - Populated '{filename}' (SQL ID: {sql_image_id}).")
                    
                    image_count += 1
        
        print("\nDatabase population complete.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if pg_conn:
            pg_conn.rollback()
    finally:
        if pg_conn:
            pg_conn.close()
            print("PostgreSQL connection closed.")
        if mongo_client:
            mongo_client.close()
            print("MongoDB connection closed.")


if __name__ == "__main__":
    populate_databases()
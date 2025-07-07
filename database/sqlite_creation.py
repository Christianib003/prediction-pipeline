#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = 'database/plant_disease_dataset.db'
DATA_DIR = './data/PlantVillage/val'


# Connect to database (creates file if not exists)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Plants (
    plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Diseases (
    disease_id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ImageMetadata (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    image_path TEXT NOT NULL,
    plant_id INTEGER,
    disease_id INTEGER,
    date_added TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES Plants (plant_id),
    FOREIGN KEY (disease_id) REFERENCES Diseases (disease_id)
)
''')

print(f"Database '{DB_PATH}' created successfully with required tables.")

# --- Insert Data Section ---

# Function to get or insert plant
def get_or_create_plant(plant_name):
    cursor.execute("SELECT plant_id FROM Plants WHERE plant_name = ?", (plant_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("INSERT INTO Plants (plant_name) VALUES (?)", (plant_name,))
    conn.commit()
    return cursor.lastrowid

# Function to get or insert disease
def get_or_create_disease(disease_name):
    cursor.execute("SELECT disease_id FROM Diseases WHERE disease_name = ?", (disease_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("INSERT INTO Diseases (disease_name) VALUES (?)", (disease_name,))
    conn.commit()
    return cursor.lastrowid

# Process folders and insert image metadata
for folder in os.listdir(DATA_DIR):
    folder_path = os.path.join(DATA_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    if '___' in folder:
        plant_raw, disease_raw = folder.split('___')
    else:
        continue

    # Clean names
    plant_name = plant_raw.replace('(maize)', 'maize').strip().capitalize()
    disease_name = disease_raw.replace('_', ' ').strip().capitalize()

    plant_id = get_or_create_plant(plant_name)
    disease_id = get_or_create_disease(disease_name)

    for img_file in os.listdir(folder_path):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(folder_path, img_file)
            cursor.execute('''
                INSERT INTO ImageMetadata (filename, image_path, plant_id, disease_id)
                VALUES (?, ?, ?, ?)
            ''', (img_file, img_path, plant_id, disease_id))

conn.commit()
conn.close()
print("Image metadata inserted successfully.")


# #!/usr/bin/env python3
# import sqlite3

# DB_PATH = 'database/plant_disease_dataset.db'

# conn = sqlite3.connect(DB_PATH)
# cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Plants (
#     plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     plant_name TEXT UNIQUE NOT NULL
# )
# ''')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Diseases (
#     disease_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     disease_name TEXT UNIQUE NOT NULL
# )
# ''')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS ImageMetadata (
#     image_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     filename TEXT NOT NULL,
#     image_path TEXT NOT NULL,
#     plant_id INTEGER,
#     disease_id INTEGER,
#     date_added TEXT DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (plant_id) REFERENCES Plants (plant_id),
#     FOREIGN KEY (disease_id) REFERENCES Diseases (disease_id)
# )
# ''')

# conn.commit()
# conn.close()

# print(f"Database '{DB_PATH}' created successfully with required tables.")

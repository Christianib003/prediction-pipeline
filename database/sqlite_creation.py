#!/usr/bin/env python3
import sqlite3

DB_PATH = 'database/plant_disease_dataset.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

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

conn.commit()
conn.close()

print(f"Database '{DB_PATH}' created successfully with required tables.")

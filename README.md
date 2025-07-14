# Plant Disease Prediction Pipeline API

This project implements a full-stack, end-to-end data pipeline designed for the automated classification of plant diseases from leaf images. It showcases a modern, robust architecture featuring a dual-database system (PostgreSQL and MongoDB), a high-performance FastAPI backend that serves a RESTful API, and a sophisticated client script that leverages a trained TensorFlow model to perform real-time predictions. The primary goal is to provide a scalable and maintainable solution for managing image metadata, executing machine learning models, and logging historical prediction data in a seamless, automated workflow.

- [Live API Link](https://prediction-pipeline.onrender.com)

- [API Documentation](https://prediction-pipeline.onrender.com/docs)

---

## Architecture Overview

This application is architected as a complete, automated pipeline where a client script orchestrates a series of interactions between hosted databases and a machine learning model, all mediated by a central, decoupled API. This separation of concerns ensures that each component is independent and can be scaled or updated without affecting the others.

The end-to-end workflow proceeds as follows:

1.  **Data Request**: The process begins when the `prediction/predict.py` script, acting as the client, initiates a `GET` request to the `/images/latest/` endpoint. This request asks the API for the metadata of the most recently added image that needs to be classified.

2.  **SQL Database Interaction**: The FastAPI application receives the request and connects to the **hosted PostgreSQL database** on Aiven. PostgreSQL is used here as the "source of truth" for structured, relational data. It queries the `image_metadata` table, leveraging its relational integrity to efficiently find the latest record and return its details, including the file path and its unique SQL ID.

3.  **Machine Learning Prediction**: Upon receiving the API response, the prediction script uses the `image_path` to load the corresponding image file from the local project directory. It then loads the pre-trained TensorFlow/Keras model (`models/optimized_cnn_model_4.keras`), which has been optimized for this task. The script preprocesses the image to the required dimensions and format before feeding it to the model to generate a definitive prediction, which includes the predicted disease class and a numerical confidence score.

4.  **Logging the Result**: With the prediction complete, the script's next responsibility is to persist this result. It makes a `POST` request to the `/predictions/` endpoint of the API, sending a JSON payload containing the prediction details and the `sql_image_id` of the image that was analyzed.

5.  **NoSQL Database Interaction**: The API receives the log data and connects to the **hosted MongoDB database** on Atlas. It uses the `sql_image_id` to quickly find the corresponding image document. MongoDB's flexible, document-based nature is ideal here; the API uses the `$push` operator to add the new prediction result into that document's `predictions` array, creating a permanent, time-stamped audit trail of every classification made for that image.

---

## Database Schema

The project leverages a dual-database strategy, using the best tool for each specific job.

### PostgreSQL (Relational)

The PostgreSQL database serves as the authoritative source for core metadata. Its relational structure, with well-defined tables and foreign key constraints, guarantees data integrity and consistency for our primary records.

**ERD Diagram:**
![ERD for SQL Database](database/docs/sql_diagram.png)

* **`plants` & `diseases` tables:** These act as normalized lookup tables, preventing data redundancy and ensuring that plant and disease names are consistent across the dataset.
* **`image_metadata` table:** This is the central table, linking plants and diseases to specific image files and storing essential metadata like file paths and creation dates.

### MongoDB (NoSQL)

The MongoDB database is chosen for its flexibility and scalability, making it perfect for storing application logs and other less-structured data. For this project, it stores a denormalized version of the image metadata alongside a growing history of predictions.

**Example `images` Document:**
```json
{
  "sql_image_id": 1,
  "filename": "image_001.jpg",
  "image_path": "data/PlantVillage/test/Tomato___Bacterial_spot/image_001.jpg",
  "plant": {
    "name": "Tomato"
  },
  "disease": {
    "name": "Bacterial spot"
  },
  "date_added": "2025-07-14T12:00:00Z",
  "predictions": [
    {
      "predicted_class_name": "Tomato___Bacterial_spot",
      "confidence_score": 0.9511,
      "prediction_date": "2025-07-15T10:30:00Z"
    }
  ]
}
```

- The `predictions` array is a key feature, allowing multiple classification results for the same image to be stored over time. This could be invaluable for tracking model performance or for more advanced analysis in the future.


## Getting Started
Follow these detailed instructions to set up and run the project on your local machine.

**Prerequisites**
- **Git**: For cloning the repository.

- **Python 3.11**: This specific version is required for compatibility with the project's dependencies, particularly TensorFlow. It is highly recommended to use pyenv to manage different Python versions on your system to avoid conflicts.

- **PlantVillage Dataset**: A local copy of the dataset is required. It should be placed in a data/ folder at the project root.

1. **Clone the Repository**
Open your terminal and clone the project from GitHub.

    ```bash
    git clone https://github.com/Christianib003/prediction-pipeline
    cd prediction-pipeline
    ```

2. **Set Up the Python Environment**
This project requires `Python 3.11`. A virtual environment is essential to isolate project dependencies and maintain a clean workspace.

    ```python
    # Set the local Python version using pyenv to avoid system-wide conflicts
    pyenv local 3.11

    # Create a new, isolated virtual environment named 'venv'
    python -m venv .venv

    # Activate the virtual environment. Your terminal prompt should change.
    source .venv/bin/activate
    ```
3. **Install Dependencies**
With the virtual environment active, use `pip` to install all the required packages listed in the `requirements.txt` file.

    ```python
    pip install -r requirements.txt
    ```
4. **Configure Environment Variables**
Create a `.env` file in the root directory. This file is crucial for storing secret credentials and configuration variables securely, keeping them separate from the source code. 

    ```python
    # Hosted PostgreSQL Connection String from your Aiven dashboard
    DATABASE_URL="postgres://user:password@host:port/database"

    # Hosted MongoDB Connection String from your Atlas dashboard
    MONGO_URL="mongodb+srv://user:password@cluster.mongodb.net/"

    # The name of your database in MongoDB Atlas
    MONGO_DB_NAME="plant_disease_db"

    # URL of your API. Use localhost for local testing or the Render URL for the deployed version.
    API_URL="[http://127.0.0.1:8000](http://127.0.0.1:8000)"
    ```

**Folder Structure**
The project is organized into distinct modules, each with a clear responsibility.

```

├── api/                  # Contains all FastAPI application source code
│   ├── app/              # Core application logic
│   │   ├── db_connectors.py  # Manages database connections
│   │   ├── models.py     # Pydantic data validation models
│   │   └── routes.py     # Defines all API endpoints
│   └── main.py           # Main FastAPI application entry point
├── data/                 # Local storage for the PlantVillage dataset
├── database/             # Scripts for database setup and management
├── docs/                 # Documentation assets like diagrams
|    └── sql_diagram.png
│   ├── sql/              # PostgreSQL-specific scripts
│   │   ├── schema.sql    # Table creation statements
│   │   ├── advanced.sql  # Stored procedure and trigger definitions
│   │   └── setup_sql.py  # Script to execute SQL files
|   |   └── verify_sql.py # Verify the correct setup of sql database
|   |   └── clear_sql.py  # Clear data from sql database
│   ├── nosql_schema.json # Documentation for the MongoDB schema
│   └── populate_databases.py # Script to populate both databases
├── models/               # Contains saved, pre-trained machine learning models
│   └── optimized_cnn_model_4.keras
├── prediction/           # Contains the client-side prediction script
│   └── predict.py
├── .gitignore            # Specifies files for Git to ignore
├── README.md             # This documentation file
└── requirements.txt      # List of Python dependencies for the project
```


## Usage
1. **Populate the Hosted Databases**
Before running the application, you must populate your hosted databases with the initial metadata from your local dataset. This script connects to both your PostgreSQL and MongoDB instances and fills them with the necessary records.

    ```
    python database/populate_databases.py
    ```

2. **Run the API Server Locally**
Start the FastAPI application server using Uvicorn. The --reload flag enables hot-reloading, which automatically restarts the server whenever you save changes to the code, greatly speeding up development.
    ```
    uvicorn api.main:app --reload
    ```

## API Endpoints
**SQL Image Metadata (CRUD)**
- `POST /images/`: Creates a new image metadata record in the PostgreSQL database.

- `GET /images/`: Retrieves a paginated list of all image records from PostgreSQL.

- `GET /images/latest/`: Fetches the single most recently added image record.

- `GET /images/{image_id}`: Fetches a specific image record by its unique ID.

- `PUT /images/{image_id}`: Updates one or more fields of an existing image record.

- `DELETE /images/{image_id}`: Deletes an image record from the database.

**MongoDB Prediction Logging**
- `POST /predictions/`: Receives prediction results and logs them by adding a new entry to the predictions array of the corresponding document in MongoDB.

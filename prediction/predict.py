import requests
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from datetime import datetime

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000"
# Use a simple relative path, assuming the script is run from the project root
MODEL_PATH = "models/optimized_cnn_model_4.keras"
IMAGE_SIZE = (128, 128)
CLASS_NAMES = [
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___healthy',
    'Potato___Early_blight',
    'Potato___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___healthy'
]

def main():
    """
    Main function to orchestrate fetching data, predicting, and logging the result.
    """
    # === 1. Fetch latest image data from the API ===
    try:
        print("Fetching latest image data from API...")
        response = requests.get(f"{API_BASE_URL}/images/latest/")
        response.raise_for_status() # Raise an exception for bad status codes
        image_data = response.json()
        print(f"Successfully fetched metadata for image ID: {image_data['image_id']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to API. Is the server running? Details: {e}")
        return

    relative_path = image_data.get("image_path")
    sql_image_id = image_data.get("image_id") # Get the SQL ID for logging

    if not relative_path:
        print("Error: API did not return an image path.")
        return
        
    full_image_path = os.path.abspath(relative_path)
    if not os.path.exists(full_image_path):
        print(f"Error: Image file not found at path: {full_image_path}")
        return

    # === 2. Load model and preprocess the image ===
    try:
        print(f"Loading model: {MODEL_PATH}")
        model = load_model(MODEL_PATH)
        
        print(f"Loading and preprocessing image: {full_image_path}")
        img = image.load_img(full_image_path, target_size=IMAGE_SIZE)
        img_array = image.img_to_array(img)
        # Normalize the image because the model does not have a Rescaling layer
        img_array /= 255.0
        img_array = np.expand_dims(img_array, axis=0)
    except Exception as e:
        print(f"Error during model or image processing: {e}")
        return

    # === 3. Make Prediction ===
    print("Making prediction...")
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction[0])
    confidence = float(np.max(prediction[0])) # Convert to standard float
    predicted_class = CLASS_NAMES[predicted_index]
    
    print("\n--- Prediction Results ---")
    print(f"  File: {os.path.basename(full_image_path)}")
    print(f"  Predicted Class: {predicted_class}")
    print(f"  Confidence: {confidence:.2%}")
    print("------------------------")

    # === 4. Log the prediction result via API ===
    try:
        print("\nLogging prediction result to database...")
        log_payload = {
            "sql_image_id": sql_image_id,
            "predicted_class_name": predicted_class,
            "confidence_score": confidence
        }
        log_response = requests.post(f"{API_BASE_URL}/predictions/", json=log_payload)
        log_response.raise_for_status()
        print("...Log successful.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to log prediction. Details: {e}")
        print(f"Response body: {log_response.text}")

if __name__ == "__main__":
    main()
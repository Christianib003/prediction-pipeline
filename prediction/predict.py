#!/usr/bin/env python3
import requests
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

API_ENDPOINT = "http://localhost:5000/images/latest" 
MODEL_PATH = "models/plant_disease_model.keras"        

response = requests.get(API_ENDPOINT)

if response.status_code != 200:
    print("Failed to fetch image path:", response.text)
    exit()

data = response.json()
img_path = data.get("image_path")

if not img_path or not os.path.exists(img_path):
    print("Invalid or missing image path:", img_path)
    exit()

print(f"Image path received: {img_path}")

# === 2. Load pre-trained Keras model ===
try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print("Failed to load model:", e)
    exit()

# === 3. Load and preprocess the image ===
try:
    img = image.load_img(img_path, target_size=(240, 240))  # Resize for model input
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
except Exception as e:
    print("Failed to load or preprocess image:", e)
    exit()

# === 4. Make prediction ===
prediction = model.predict(img_array)

# === 5. Interpret prediction ===
if prediction.shape[1] == 1:  # Binary classification
    label = "unhealthy" if prediction[0][0] > 0.5 else "healthy"
    confidence = prediction[0][0]
else:  # Multiclass prediction
    class_labels = [
        'Corn_(maize)__Common_rust',
        'Corn_(maize)__healthy',
        'Potato__Early_blight',
        'Potato__healthy',
        'Tomato__Bacterial_spot',
        'Tomato__healthy'
    ]

    predicted_index = np.argmax(prediction)
    label = class_labels[predicted_index]
    confidence = prediction[0][predicted_index]

print(f"Prediction: {label} (Confidence: {confidence:.2f})")

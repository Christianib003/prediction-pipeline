#!/usr/bin/env python3
import requests
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

API_ENDPOINT = "http://127.0.0.1:8000/images/latest" 
MODEL_PATH = "prediction/model/plant_deseases.keras"


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

try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")

except Exception as e:
    print("Failed to load model:", e)
    exit()
try:
    img = image.load_img(img_path, target_size=(128, 128), color_mode='rgb') 
    img_array = image.img_to_array(img)       
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0) 

except Exception as e:
    print("Failed to load or preprocess image:", e)
    print("Model expects input shape:", model.input_shape)

    print("Input you're sending:", img_array.shape)

    exit()


prediction = model.predict(img_array)

# === 5. Interpret prediction ===
CLASS_NAMES = [
    'Corn_(maize)__Common_rust',
    'Corn_(maize)__healthy',
    'Potato__Early_blight',
    'Potato__healthy',
    'Tomato__Bacterial_spot',
    'Tomato__healthy'
]

# predicted_index = np.argmax(prediction)
# label = class_labels[predicted_index]
# confidence = prediction[0][predicted_index]

# print(f"Prediction: {label} (Confidence: {confidence:.2f})")

predicted_index = np.argmax(prediction[0])
label = CLASS_NAMES[predicted_index]
confidence = prediction[0][predicted_index]

print("\n- Prediction Results -")
print(f"Predicted Class: {label}")
print(f"Confidence: {confidence:.2f}")

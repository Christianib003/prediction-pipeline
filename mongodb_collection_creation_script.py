#!/usr/bin/env python3

import os

# Root dataset directory
DATASET_DIR = "data/PlantVillage"

# Main loop
print("Displaying first 10 image locations from the dataset:")
print("=" * 50)

image_count = 0
max_images_to_display = 10

for split in ["train", "val"]:
    split_dir = os.path.join(DATASET_DIR, split)
    if not os.path.exists(split_dir):
        print(f"⚠️ Directory '{split_dir}' not found. Skipping.")
        continue

    for class_dir in os.listdir(split_dir):
        class_path = os.path.join(split_dir, class_dir)
        if not os.path.isdir(class_path):
            continue

        for img_file in os.listdir(class_path):
            img_path = os.path.join(class_path, img_file)
            
            if not os.path.isfile(img_path):
                continue
            
            # Print the image location
            print(f"{image_count + 1}. {img_path}")
            image_count += 1
            
            if image_count >= max_images_to_display:
                break
        
        if image_count >= max_images_to_display:
            break
    
    if image_count >= max_images_to_display:
        break

print("=" * 50)
print(f"Displayed {image_count} image locations")
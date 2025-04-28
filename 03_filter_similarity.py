# This script filters images based on their sharpness using the Laplacian variance method.
# It checks the center of each image and saves only the sharp images to a new folder.
# Additionally, it detects duplicate images based on perceptual hashing and sorts sharp images into folders.

import cv2
import os
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm

# Define folder paths
base_folder = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
source_folder = os.path.join(base_folder, "rawpictures")
filtered_folder = os.path.join(source_folder, "FilteredImages")
duplicates_folder = os.path.join(source_folder, "duplicates")

# Create folders if they don't exist
os.makedirs(filtered_folder, exist_ok=True)
os.makedirs(duplicates_folder, exist_ok=True)

# Blur threshold
BLUR_THRESHOLD = 20.0

# Threshold for image similarity
HASH_DIFF_THRESHOLD = 8  

def is_blurry_center(image):
    """
    Check if the center of the image is blurry using the Laplacian variance.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    x_start = int(w * 0.375)
    y_start = int(h * 0.375)
    x_end = int(w * 0.625)
    y_end = int(h * 0.625)
    center = gray[y_start:y_end, x_start:x_end]
    return cv2.Laplacian(center, cv2.CV_64F).var() < BLUR_THRESHOLD

def is_similar_image(image1_hash, seen_hashes, threshold):
    """
    Check if an image is similar to previously seen images based on perceptual hashing.
    """
    for saved_hash in seen_hashes:
        if abs(image1_hash - saved_hash) <= threshold:
            return True
    return False

def filter_sharp_images():
    """
    Filter images based on sharpness and save only sharp images.
    """
    image_extensions = [".png", ".jpg", ".jpeg"]
    files = [f for f in os.listdir(source_folder) if os.path.splitext(f)[1].lower() in image_extensions]

    for file in tqdm(files, desc="Filtering sharp images"):
        filepath = os.path.join(source_folder, file)
        image = cv2.imread(filepath)

        if image is None:
            print(f"⚠️ Unable to read {file}, skipping.")
            continue

        if not is_blurry_center(image):
            cv2.imwrite(os.path.join(filtered_folder, file), image)

    print("🎉 Filtering completed!")

def compare_and_move_images():
    """
    Compare images, rename them, and sort them into folders of 1000 images each.
    """
    image_list = [f for f in os.listdir(source_folder) if f.lower().endswith(".png")]
    seen_hashes = []
    duplicate_count = 1
    sharp_count = 1
    folder_number = 1

    # Start with the first target folder
    current_folder = os.path.join(source_folder, f"Set_{folder_number:03}")
    os.makedirs(current_folder, exist_ok=True)

    for filename in tqdm(sorted(image_list), desc="Detecting and sorting similar images"):
        filepath = os.path.join(source_folder, filename)

        try:
            image = Image.open(filepath)
            image_hash = imagehash.phash(image)

            if is_similar_image(image_hash, seen_hashes, HASH_DIFF_THRESHOLD):
                new_name = f"threshold_{HASH_DIFF_THRESHOLD}_failed_duplicate_{duplicate_count:05}.png"
                shutil.move(filepath, os.path.join(duplicates_folder, new_name))
                print(f"➡️ Duplicate moved and renamed: {new_name}")
                duplicate_count += 1
            else:
                if sharp_count > folder_number * 1000:
                    folder_number += 1
                    current_folder = os.path.join(source_folder, f"Set_{folder_number:03}")
                    os.makedirs(current_folder, exist_ok=True)

                new_name = f"threshold_{HASH_DIFF_THRESHOLD}_pass_sorted_{sharp_count:05}.png"
                target_path = os.path.join(current_folder, new_name)
                shutil.move(filepath, target_path)

                seen_hashes.append(image_hash)
                sharp_count += 1
                print(f"✅ Sharp image moved: {new_name} to {current_folder}")

        except Exception as e:
            print(f"❌ Error with {filename}: {e}")

if __name__ == "__main__":
    try:
        filter_sharp_images()
        compare_and_move_images()
    except Exception as e:
        print(f"💥 Error during processing: {e}")

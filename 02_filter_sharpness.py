# This script filters images based on their sharpness using the Laplacian variance method.
# It checks the center of each image and saves only the sharp images to a new folder.

import cv2
import os
from tqdm import tqdm

# Define folder paths
base_folder = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
source_folder = os.path.join(base_folder, "rawpictures")
filtered_folder = os.path.join(source_folder, "FilteredImages")

# Create folder for filtered images if it doesn't exist
os.makedirs(filtered_folder, exist_ok=True)

# Blur threshold
BLUR_THRESHOLD = 20.0

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

if __name__ == "__main__":
    try:
        filter_sharp_images()
    except Exception as e:
        print(f"💥 Error during processing: {e}")

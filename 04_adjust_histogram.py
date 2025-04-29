# This script optimizes the brightness and contrast of filtered images
# based on their histogram. The optimized images are saved in a new folder.

import cv2
import os
from tqdm import tqdm

# Define folder paths
base_folder = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
source_folder = os.path.join(base_folder, "FilteredImages")
optimized_folder = os.path.join(source_folder, "OptimizedImages")

# Create target folder if it doesn't exist
os.makedirs(optimized_folder, exist_ok=True)

def optimize_image_histogram(image):
    """
    Optimizes the brightness and contrast of an image based on its histogram.
    """
    # Convert the image to YUV color space
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y_channel, u_channel, v_channel = cv2.split(yuv_image)

    # Apply histogram equalization on the Y channel (brightness)
    y_channel = cv2.equalizeHist(y_channel)

    # Merge the channels back and convert to BGR color space
    optimized_image = cv2.merge((y_channel, u_channel, v_channel))
    return cv2.cvtColor(optimized_image, cv2.COLOR_YUV2BGR)

def process_images():
    """
    Optimizes the brightness and contrast of all images in the source folder.
    """
    image_extensions = [".png", ".jpg", ".jpeg"]
    files = [f for f in os.listdir(source_folder) if os.path.splitext(f)[1].lower() in image_extensions]

    for file in tqdm(files, desc="Optimizing images"):
        filepath = os.path.join(source_folder, file)
        image = cv2.imread(filepath)

        if image is None:
            print(f"⚠️ Unable to read {file}, skipping.")
            continue

        # Optimize the image
        optimized_image = optimize_image_histogram(image)

        # Save the optimized image
        cv2.imwrite(os.path.join(optimized_folder, file), optimized_image)

    print("🎉 Optimization completed!")

if __name__ == "__main__":
    try:
        process_images()
    except Exception as e:
        print(f"💥 Error during processing: {e}")
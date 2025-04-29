# This script filters images based on their similarity using perceptual hashing.
# It checks for duplicates and moves them to a separate folder, while also renaming the images.
# It sorts the images into folders of 1000 images each, renaming them in the process.

import os
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm

# Folder paths
source_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FilteredImages")
duplicates_folder = os.path.join(source_folder, "duplicates")

# Create target folder if it doesn't exist
os.makedirs(duplicates_folder, exist_ok=True)

# Threshold for image similarity
HASH_DIFF_THRESHOLD = 8  

# Helper function to check for duplicate images
def is_similar_image(image1_hash, seen_hashes, threshold):
    for saved_hash in seen_hashes:
        if abs(image1_hash - saved_hash) <= threshold:
            return True
    return False

# Compare images, rename them, and sort them into folders of 1000 images each
def compare_and_move_images():
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
    compare_and_move_images()

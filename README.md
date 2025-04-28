# Photogrammetry-Tools
This is a collection of some simple tools I created to help me with my photogrammetry workflows and sorting through large amounts of data.

These tools are mainly designed to:
1. Convert videos into pictures.
2. Filter pictures based on sharpness.
3. Use a hashing algorithm to separate similar pictures, reducing the total number of images while maintaining quality.

The tools are easy to use but require running through the terminal. Progress bars are implemented to monitor the process, which is essential for large datasets to ensure the tools are working.

These tools are written in Python and tested on Windows and Linux (NixOS).

## Requirements
- **Python 3.13** or higher
- **Node.js** (if needed for additional tools)
- **A lot of free space**: Depending on the video data, you might need a lot of space for `.png` images. 30GB Video was 800GB Pictures after the export.

These scripts are created to work within a defined folder structure. You need to **change the scripts to your local paths** so they can work correctly. These places are clearly labeled in the code itself:



### Installation Instructions

#### Windows
1. Install Python:
   - Download and install Python from [python.org](https://www.python.org/).
   - Make sure to check the box to add Python to your PATH during installation.

2. Install required Python packages:
   Open a terminal (Command Prompt or PowerShell) and run:
   ```bash
   pip install opencv-python tqdm pillow imagehash
   ```

3. Install FFmpeg:
   - Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/).
   - Add FFmpeg to your PATH by following the instructions on the FFmpeg website.

#### Linux
1. Install Python:
   - For Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```
   - For Fedora:
     ```bash
     sudo dnf install python3 python3-pip
     ```

2. Install required Python packages:
   ```bash
   pip3 install opencv-python tqdm pillow imagehash
   ```

3. Install FFmpeg:
   - For Ubuntu/Debian:
     ```bash
     sudo apt install ffmpeg
     ```
   - For Fedora:
     ```bash
     sudo dnf install ffmpeg
     ```

##### NixOS
1. Install Python and required packages using `nix-shell`:
   ```bash
   nix-shell -p python3 python3Packages.pip python3Packages.opencv4 python3Packages.tqdm python3Packages.pillow python3Packages.imagehash
   ```

2. Install FFmpeg:
   ```bash
   nix-shell -p ffmpeg
   ```

### Additional Notes
- **FFmpeg** is required for the `01_convert_video_to_picture.py` script to extract frames from videos. Make sure it is installed and accessible from the terminal.
- Ensure that you have sufficient disk space for processing large datasets.
- Adjust the paths in the scripts to match your local folder structure. These places are clearly labeled in the code.
- The tools are designed to work with a specific folder structure. Ensure that the required folders exist before running the scripts.


## Guide

### 1. `01_convert_video_to_picture.py`
- **Purpose**: Converts videos into individual image frames.
- **How it works**:
  - Extracts frames from videos using FFmpeg.
  - Saves the frames as `.png` images in the `rawpictures` folder.
- **Usage**:
  1. Place your videos in the `rawvideos` folder.
  2. Run the script:
     ```bash
     python 01_convert_video_to_picture.py
     ```
  3. The extracted frames will be saved in subfolders inside `rawpictures`.

### 2. `02_filter_sharpness.py`
- **Purpose**: Filters images based on their sharpness.
- **How it works**:
  - Uses the Laplacian variance method to check the sharpness of the center of each image.
  - Saves only sharp images to the `FilteredImages` folder.
- **Usage**:
  1. Ensure the `rawpictures` folder contains the images to be filtered.
  2. Run the script:
     ```bash
     python 02_filter_sharpness.py
     ```
  3. Sharp images will be saved in the `FilteredImages` folder.

### 3. `03_filter_similarity.py`
- **Purpose**: Filters out similar images using perceptual hashing.
- **How it works**:
  - Compares images in the `FilteredImages` folder using a hashing algorithm.
  - Moves duplicate images to the `duplicates` folder.
  - Sorts unique images into subfolders of 1000 images each.
- **Usage**:
  1. Ensure the `FilteredImages` folder contains the images to be processed.
  2. Run the script:
     ```bash
     python 03_filter_similarity.py
     ```
  3. Unique images will be sorted into subfolders, and duplicates will be moved to the `duplicates` folder.

---

### Workflow
1. **Step 1**: Use `01_convert_video_to_picture.py` to extract frames from videos.
2. **Step 2**: Use `02_filter_sharpness.py` to filter out blurry images.
3. **Step 3**: Use `03_filter_similarity.py` to remove duplicate or similar images and organize the remaining ones.

This workflow ensures that you end up with a clean, sharp, and unique set of images for your photogrammetry projects.
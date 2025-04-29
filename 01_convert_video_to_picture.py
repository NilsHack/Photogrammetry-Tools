# This script converts videos to images using FFmpeg.
# It extracts frames from each video and saves them in a specified output folder.

import os
import subprocess

# Define source and output folders
base_folder = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
source_folder = os.path.join(base_folder, "rawvideos")
output_folder = os.path.join(base_folder, "rawpictures")

# Supported video file extensions
video_extensions = [".mp4", ".mov", ".avi", ".mkv"]

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def convert_videos_to_images():
    # Get a list of video files in the source folder
    video_files = [f for f in os.listdir(source_folder) if os.path.splitext(f)[1].lower() in video_extensions]

    total_videos = len(video_files)  # Total number of videos
    for index, video_file in enumerate(video_files, start=1):
        video_path = os.path.join(source_folder, video_file)
        video_name = f"Video_{index:02}"

        # Create a folder for the images of this video
        video_output_folder = os.path.join(output_folder, video_name)
        os.makedirs(video_output_folder, exist_ok=True)

        # FFmpeg command to extract frames from the video
        ffmpeg_command = [
            "ffmpeg",
            "-i", video_path,  # Input video file
            os.path.join(video_output_folder, f"{video_name}_Frame_%04d.png")  # Output image format
        ]

        try:
            # Execute the FFmpeg command
            subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Processed {index}/{total_videos}", end='\r')  # Update progress in the same line
        except subprocess.CalledProcessError as e:
            print(f"\nError processing {video_file}: {e.stderr.decode('utf-8')}")

    print("\nProcess finished")  # Move to a new line after completion

if __name__ == "__main__":
    try:
        convert_videos_to_images()
    except Exception as e:
        print(f"Error: {e}")
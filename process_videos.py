# CONVERT VIDEOS TO MP3
import os
import subprocess

os.makedirs("audios", exist_ok=True)

video_extensions = (".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm")

for file in os.listdir("videos"):
    video_path = os.path.join("videos", file)

    # check valid video file
    if os.path.isfile(video_path) and file.lower().endswith(video_extensions):

        file_name = os.path.splitext(file)[0]
        output_path = os.path.join("audios", f"{file_name}.mp3")

        print(f"Processing: {file}")

        try:
            subprocess.run([
                "ffmpeg",
                "-y",              # overwrite automatically
                "-i", video_path,
                output_path
            ], check=True)

        except subprocess.CalledProcessError:
            print(f"Error processing: {file}")

    else:
        print(f"Skipping: {file}")
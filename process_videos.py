#CONVERT VIDEOS TO MP3
import os
import subprocess

os.makedirs("audios", exist_ok=True)

files = os.listdir("videos")

for file in files:
    # remove extension
    file_name = os.path.splitext(file)[0]

    print(file_name)

    subprocess.run([
        "ffmpeg",
        "-i", f"videos/{file}",
        f"audios/{file_name}.mp3"
    ])
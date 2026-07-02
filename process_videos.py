import os
import subprocess


def process_videos(video_path=None):
    os.makedirs("audios", exist_ok=True)

    video_extensions = (".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm")

    # New Upload Mode
    if video_path is not None:

        file = os.path.basename(video_path)

        if not file.lower().endswith(video_extensions):
            print("Invalid video format.")
            return None

        file_name = os.path.splitext(file)[0]
        output_path = os.path.join("audios", f"{file_name}.mp3")

        print(f"Processing: {file}")

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    video_path,
                    output_path,
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )

        except FileNotFoundError:
            print("FFmpeg is not installed or not found in PATH.")
            return None

        except subprocess.CalledProcessError as e:
            print(f"Error processing {file}")
            print(e.stderr.decode(errors="ignore"))
            return None

        return output_path

    # Old Mode
    for file in os.listdir("videos"):

        current_video_path = os.path.join("videos", file)

        if os.path.isfile(current_video_path) and file.lower().endswith(video_extensions):

            file_name = os.path.splitext(file)[0]
            output_path = os.path.join("audios", f"{file_name}.mp3")

            print(f"Processing: {file}")

            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        current_video_path,
                        output_path,
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                )

            except FileNotFoundError:
                print("FFmpeg is not installed or not found in PATH.")
                continue

            except subprocess.CalledProcessError as e:
                print(f"Error processing {file}")
                print(e.stderr.decode(errors="ignore"))

        else:
            print(f"Skipping: {file}")


if __name__ == "__main__":
    process_videos()
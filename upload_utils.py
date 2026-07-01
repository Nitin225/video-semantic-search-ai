import os

def save_uploaded_video(uploaded_file):

    os.makedirs("videos", exist_ok=True)

    video_path = os.path.join("videos", uploaded_file.name)

    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return video_path
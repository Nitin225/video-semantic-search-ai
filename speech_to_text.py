import whisper
import json
import os

TARGET_WORDS = 120


def merge_segments(segments, target_words=TARGET_WORDS):
    merged = []

    current_text = []
    current_words = 0
    start = None
    end = None
    source = None

    for segment in segments:

        text = segment["text"].strip()

        if not text:
            continue

        words = len(text.split())

        if start is None:
            start = segment["start"]
            source = segment["source"]

        current_text.append(text)
        current_words += words
        end = segment["end"]

        if current_words >= target_words:

            merged.append({
                "source": source,
                "start": start,
                "end": end,
                "text": " ".join(current_text)
            })

            current_text = []
            current_words = 0
            start = None
            end = None
            source = None

    if current_text:

        merged.append({
            "source": source,
            "start": start,
            "end": end,
            "text": " ".join(current_text)
        })

    return merged


def process_audio(audio_path, model):

    file = os.path.basename(audio_path)

    result = model.transcribe(
        audio=audio_path,
        task="translate",
        fp16=False
    )

    segments = []

    for segment in result["segments"]:

        segments.append({
            "source": file,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    print(f"{file}")
    print(f"Original Whisper Segments : {len(segments)}")

    chunks = merge_segments(segments)

    print(f"Merged Chunks            : {len(chunks)}")

    json_name = os.path.splitext(file)[0] + ".json"
    json_path = os.path.join("json_files", json_name)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    return json_path


def speech_to_text(audio_path=None):

    model = whisper.load_model("small")

    os.makedirs("json_files", exist_ok=True)

    if audio_path is not None:

        if not audio_path.lower().endswith((".mp3", ".wav", ".m4a")):
            print("Invalid audio format.")
            return None

        return process_audio(audio_path, model)

    for file in os.listdir("audios"):

        if not file.lower().endswith((".mp3", ".wav", ".m4a")):
            continue

        current_audio = os.path.join("audios", file)

        process_audio(current_audio, model)

    print("All audios processed!")


if __name__ == "__main__":
    speech_to_text()
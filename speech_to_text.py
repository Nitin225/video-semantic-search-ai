import whisper
import json
import os


def speech_to_text(audio_path=None):
    model = whisper.load_model("small")

    os.makedirs("json_files", exist_ok=True)

    if audio_path is not None:

        file = os.path.basename(audio_path)

        if not file.lower().endswith((".mp3", ".wav", ".m4a")):
            print("Invalid audio format.")
            return None

        result = model.transcribe(
            audio=audio_path,
            task="translate",
            fp16=False
        )

        chunks = []

        for segment in result["segments"]:
            chunks.append({
                "source": file,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        print(f"{file} -> {len(chunks)} segments")

        json_name = os.path.splitext(file)[0] + ".json"
        json_path = os.path.join("json_files", json_name)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=4, ensure_ascii=False)

        return json_path

    audios = os.listdir("audios")

    for audio in audios:

        if not audio.lower().endswith((".mp3", ".wav", ".m4a")):
            continue

        current_audio_path = os.path.join("audios", audio)

        result = model.transcribe(
            audio=current_audio_path,
            task="translate",
            fp16=False
        )

        chunks = []

        for segment in result["segments"]:
            chunks.append({
                "source": audio,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        print(f"{audio} -> {len(chunks)} segments")

        json_name = os.path.splitext(audio)[0] + ".json"

        with open(
            os.path.join("json_files", json_name),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(chunks, f, indent=4, ensure_ascii=False)

    print("All audios processed!")


if __name__ == "__main__":
    speech_to_text()
import whisper
import json
import os

model = whisper.load_model("small")

audios = os.listdir("audios")

for audio in audios:
    if not audio.lower().endswith((".mp3", ".wav", ".m4a")):
        continue
    audio_path = os.path.join("audios", audio)
    result = model.transcribe(
        audio=audio_path,
        task="translate", 
        fp16=False
    )

    # print(result["segments"])
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
            

    os.makedirs("json_files", exist_ok=True)
    with open(f"json_files/{json_name}", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)
            
print("All audios processed!")
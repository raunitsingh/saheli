import whisper

model = whisper.load_model("small")

def transcribe(audio_path: str):
    result = model.transcribe(audio_path, language="hi")
    return result["text"]

if __name__ == "__main__":
    text = transcribe("audio/sample.wav")
    print(text)
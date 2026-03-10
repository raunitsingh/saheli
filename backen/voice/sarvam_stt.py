import requests
import os
from dotenv import load_dotenv
from speech.whisper_stt import transcribe as whisper_transcribe

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")
URL = "https://api.sarvam.ai/speech-to-text"


def transcribe_audio(audio_path):

    headers = {
        "api-subscription-key": API_KEY
    }

    try:

        with open(audio_path, "rb") as audio_file:

            files = {
                "file": ("audio.wav", audio_file, "audio/wav")
            }

            data = {
                "model": "saaras:v3",
                "language_code": "hi-IN",
                "mode": "codemix"
            }

            response = requests.post(
                URL,
                headers=headers,
                files=files,
                data=data,
                timeout=10
            )

        result = response.json()

        transcript = result.get("transcript")

        if transcript:
            print("Using Sarvam STT")
            return transcript

        raise Exception("Empty transcript")

    except Exception as e:

        print("Sarvam failed → switching to Whisper")
        print("Reason:", e)

        return whisper_transcribe(audio_path)
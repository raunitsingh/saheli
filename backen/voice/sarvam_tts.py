import requests
import os
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")
URL = "https://api.sarvam.ai/text-to-speech"


def speak_text(text):

    headers = {
        "api-subscription-key": API_KEY
    }

    data = {
        "text": text,
        "voice": "ananya",
        "language_code": "hi-IN"
    }

    try:

        response = requests.post(URL, headers=headers, json=data, timeout=10)

        with open("response.mp3", "wb") as f:
            f.write(response.content)

        print("Using Sarvam TTS")

    except Exception as e:

        print("Sarvam TTS failed → switching to local TTS")
        print("Reason:", e)

        engine = pyttsx3.init()

        engine.say(text)
        engine.runAndWait()
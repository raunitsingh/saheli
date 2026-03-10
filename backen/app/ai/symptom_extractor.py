import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=API_KEY)


def extract_symptoms(text: str) -> dict:
    prompt = f"""You are a clinical assistant helping ASHA workers document patient symptoms in rural India.

Analyze this patient statement and extract medical information.
Patient said: "{text}"

Respond ONLY with a valid JSON object. No explanation, no markdown, no code blocks. Just raw JSON.

{{
  "symptoms": ["list of symptoms mentioned"],
  "duration": "how long symptoms have been present",
  "severity": "mild or moderate or severe",
  "body_parts_affected": ["list of affected body parts"],
  "possible_condition": "most likely condition based on symptoms",
  "referral_needed": true or false,
  "referral_reason": "reason if referral needed, else null"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    # Clean markdown fences if present
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "JSON parsing failed", "raw_response": raw}


if __name__ == "__main__":
    test_cases = [
        "मुझे तीन दिन से तेज बुखार है और शरीर दर्द कर रहा है",
        "I have been coughing at night for 2 weeks and losing weight",
        "बच्चे को उल्टी हो रही है और बुखार है, कल से खाना नहीं खाया"
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"\n--- Test {i} ---")
        print(f"Input: {text}")
        result = extract_symptoms(text)
        print("Output:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
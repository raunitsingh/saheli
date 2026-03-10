from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def score_risk(soap_note):

    prompt = f"""
You are a medical triage assistant.

Analyze the SOAP note below.

SOAP NOTE:
{soap_note}

Return:

Risk Level: Low / Medium / High
Red Flags:
Recommended Action:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
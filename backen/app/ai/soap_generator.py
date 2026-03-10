from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_soap(interview_data):

    prompt = f"""
You are a clinical assistant.

Convert the following interview data into a SOAP medical note.

Interview Data:
{interview_data}

Return structured output:

Subjective:
Objective:
Assessment:
Plan:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
import sys
import os
import json
from datetime import datetime

# allow project root imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from voice.sarvam_stt import transcribe_audio
from voice.sarvam_tts import speak_text

from app.ai.symptom_detector import detect_symptoms
from app.ai.interview_engine import InterviewEngine
from app.ai.clinical_reasoning import analyze_case
from app.ai.soap_generator import generate_soap
from app.ai.risk_scorer import score_risk

from database.supabase_client import supabase


# ---------------------------------------------------
# Offline Queue (for no internet)
# ---------------------------------------------------

OFFLINE_QUEUE_FILE = "offline_queue.json"


def save_offline(data):

    if not os.path.exists(OFFLINE_QUEUE_FILE):
        with open(OFFLINE_QUEUE_FILE, "w") as f:
            json.dump([], f)

    with open(OFFLINE_QUEUE_FILE, "r") as f:
        queue = json.load(f)

    queue.append(data)

    with open(OFFLINE_QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

    print("Visit stored in offline queue.")


# ---------------------------------------------------
# Extract Risk Level from LLM output
# ---------------------------------------------------

def extract_risk_level(risk_text):

    risk_text = risk_text.lower()

    if "high" in risk_text:
        return "high"

    if "medium" in risk_text:
        return "medium"

    if "low" in risk_text:
        return "low"

    return "unknown"


# ---------------------------------------------------
# Save Visit to Supabase
# ---------------------------------------------------

def save_visit(patient_id, transcript, symptoms, interview_data, analysis, soap_note, risk_text):

    risk_level = extract_risk_level(risk_text)

    visit_data = {
        "patient_id": patient_id,
        "transcript": transcript,
        "symptoms": symptoms,
        "interview_data": interview_data,
        "possible_condition": analysis["possible_conditions"][0] if analysis["possible_conditions"] else None,
        "severity": risk_level,
        "risk_level": risk_level,
        "referral_needed": analysis["referral_needed"],
        "referral_reason": analysis["reason"],
        "soap_note": soap_note,
        "created_at": datetime.utcnow().isoformat()
    }

    try:

        print("\nSaving visit to Supabase...")

        supabase.table("visits").insert(visit_data).execute()

        print("Visit saved successfully.")

    except Exception as e:

        print("Supabase failed → saving locally.")
        print("Error:", e)

        save_offline(visit_data)


# ---------------------------------------------------
# Main Voice Assistant Pipeline
# ---------------------------------------------------

def run_voice_assistant(audio_file):

    print("\nListening to user audio...")

    transcript = transcribe_audio(audio_file)

    print("\nUser said:", transcript)

    symptoms = detect_symptoms(transcript)

    if not symptoms:

        speak_text("मुझे आपके लक्षण समझ नहीं आए, कृपया फिर से बताएं")
        return

    print("\nDetected symptoms:", symptoms)

    engine = InterviewEngine()

    interview_results = {}

    # -----------------------------------------------
    # AI Guided Interview
    # -----------------------------------------------

    for symptom in symptoms:

        print(f"\nStarting interview for: {symptom}")

        question = engine.start_interview(symptom)

        while question:

            print("\nAI:", question)

            speak_text(question)

            response_audio = input("\nEnter next audio file path: ")

            user_response = transcribe_audio(response_audio)

            print("User:", user_response)

            question = engine.next_question(user_response)

        results = engine.get_results()

        interview_results[symptom] = results

    print("\nCollected Interview Data:")
    print(interview_results)

    # -----------------------------------------------
    # Clinical Reasoning
    # -----------------------------------------------

    print("\nRunning Clinical Reasoning...")

    analysis = analyze_case(interview_results)

    print("\nClinical Analysis:")
    print(analysis)

    # -----------------------------------------------
    # Generate SOAP Note
    # -----------------------------------------------

    print("\nGenerating SOAP note...")

    soap_note = generate_soap(interview_results)

    print("\nSOAP NOTE:\n")
    print(soap_note)

    # -----------------------------------------------
    # Risk Scoring
    # -----------------------------------------------

    print("\nCalculating Risk Level...")

    risk_text = score_risk(soap_note)

    print("\nRISK ANALYSIS:\n")
    print(risk_text)

    # -----------------------------------------------
    # Save Visit
    # -----------------------------------------------

    patient_id = None  # optional

    save_visit(
        patient_id,
        transcript,
        interview_results,
        interview_results,
        analysis,
        soap_note,
        risk_text
    )

    speak_text("आपकी रिपोर्ट तैयार है। धन्यवाद।")


# ---------------------------------------------------
# Entry Point
# ---------------------------------------------------

if __name__ == "__main__":

    audio = input("Enter patient audio file: ")

    run_voice_assistant(audio)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.symptom_detector import detect_symptoms
from ai.interview_engine import InterviewEngine
from ai.clinical_reasoning import analyze_case


def run_interview(patient_text):

    print("\nPatient says:")
    print(patient_text)

    symptoms = detect_symptoms(patient_text)

    if not symptoms:
        print("\nNo clear symptoms detected.")
        return

    print("\nDetected symptoms:", symptoms)

    engine = InterviewEngine()

    interview_results = {}

    for symptom in symptoms:

        print(f"\nStarting interview for symptom: {symptom}")

        question = engine.start_interview(symptom)

        while question:

            print("\nAI:", question)

            answer = input("Patient: ")

            question = engine.next_question(answer)

        results = engine.get_results()

        interview_results[symptom] = results

        print("\nInterview completed.")

    print("\nCollected Interview Data:")
    print(interview_results)

    print("\nRunning Clinical Reasoning...\n")

    analysis = analyze_case(interview_results)

    print("Clinical Analysis:")
    print(analysis)


if __name__ == "__main__":

    text = input("Enter patient description: ")

    run_interview(text)
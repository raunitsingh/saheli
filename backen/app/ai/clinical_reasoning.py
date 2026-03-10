## LLM + medical rules

from knowledge_base.retriever import retrieve_guidelines
from .symptom_detector import detect_symptoms


def analyze_case(interview_data):

    risk_flags = []
    possible_conditions = []
    guidelines = retrieve_guidelines("tuberculosis symptoms cough blood sputum")

    # check cough related red flags
    if "cough" in interview_data:

        cough_data = interview_data["cough"]

        duration = cough_data.get("How long have you been coughing?", "")
        blood = cough_data.get("Have you noticed blood in the sputum?", "")

        if "week" in duration or "blood" in blood or "yes" in blood:
            risk_flags.append("possible TB indicator")
            possible_conditions.append("tuberculosis")

    # check fever conditions
    if "fever" in interview_data:

        fever_data = interview_data["fever"]

        duration = fever_data.get("How long have you had the fever?", "")

        if "3" in duration or "4" in duration or "5" in duration:
            possible_conditions.append("viral infection")

    # determine referral
    referral_needed = False
    reason = None

    if risk_flags:
        referral_needed = True
        reason = ", ".join(risk_flags)

    result = {

        "possible_conditions": possible_conditions,
        "risk_flags": risk_flags,
        "referral_needed": referral_needed,
        "reason": reason,
        "guideline_evidence": guidelines

    }

    return result
import json
from database.supabase_client import supabase


def save_visit(patient_id, transcript, interview_data, soap, risk, referral):

    data = {
        "patient_id": patient_id,
        "transcript": transcript,
        "interview_data": interview_data,
        "soap_note": soap,
        "risk_level": risk,
        "referral_needed": referral
    }

    response = supabase.table("visits").insert(data).execute()

    return response
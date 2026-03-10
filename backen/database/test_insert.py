from supabase_client import supabase

patient = supabase.table("patients").insert({
    "name": "Ravi",
    "age": 40,
    "gender": "male",
    "village": "Rampur"
}).execute()

patient_id = patient.data[0]["id"]

visit = supabase.table("visits").insert({
    "patient_id": patient_id,
    "transcript": "I have fever and headache",
    "symptoms": {"fever": True, "headache": True},
    "possible_condition": "viral infection",
    "severity": "medium",
    "referral_needed": False
}).execute()

print("Patient:", patient.data)
print("Visit:", visit.data)
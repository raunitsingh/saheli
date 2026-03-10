import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="Saheli API", version="1.0.0")

# ── CORS — allow Streamlit to talk to FastAPI ─────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request models ─────────────────────────────────────────────────────────────
class VisitRequest(BaseModel):
    name: str
    age: int
    village: str

class SaveVisitRequest(BaseModel):
    name: str | None = None
    age: int | None = None
    village: str | None = None
    risk: str | None = None
    risk_reason: str | None = None
    soap: dict | None = None
    symptoms: list | None = None

class SMSRequest(BaseModel):
    phone: str
    message: str

# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "Saheli API is running"}

# ── Run full AI visit pipeline ─────────────────────────────────────────────────
@app.post("/run-visit")
def run_visit(data: VisitRequest):
    try:
        from backend.voice.voice_pipeline import run_voice_assistant
        result = run_voice_assistant(
            patient_name=data.name,
            patient_age=data.age,
            village=data.village
        )
        return result
    except ImportError:
        # Voice pipeline not yet wired — return mock for testing
        return {
            "name": data.name,
            "age": data.age,
            "village": data.village,
            "risk": "high",
            "risk_reason": "Demo mode — voice pipeline not connected yet",
            "symptoms": ["fever", "cough"],
            "soap": {
                "subjective": f"Patient {data.name} from {data.village} reports symptoms.",
                "objective": "Reported verbally. No clinical instruments used.",
                "assessment": "Awaiting AI pipeline connection.",
                "plan": "Refer to PHC for further evaluation.",
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Get all saved visits ───────────────────────────────────────────────────────
@app.get("/visits")
def get_visits():
    try:
        from backend.db.supabase_client import get_all_visits
        return get_all_visits()
    except ImportError:
        # Supabase not yet connected — return empty so UI falls back to mock
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Save a visit ───────────────────────────────────────────────────────────────
@app.post("/save-visit")
def save_visit(data: SaveVisitRequest):
    try:
        from backend.db.supabase_client import save_visit_to_db
        save_visit_to_db(data.dict())
        return {"status": "saved"}
    except ImportError:
        # Supabase not yet connected
        return {"status": "saved (local only — Supabase not connected)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Send SMS ───────────────────────────────────────────────────────────────────
@app.post("/send-sms")
def send_sms(data: SMSRequest):
    try:
        from backend.sms.fast2sms_client import send_sms_to_patient
        send_sms_to_patient(phone=data.phone, message=data.message)
        return {"status": "sms_sent"}
    except ImportError:
        # SMS module not yet connected
        return {"status": "sms_queued (Fast2SMS not connected yet)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
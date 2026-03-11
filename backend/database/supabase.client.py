import os
from supabase import create_client
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
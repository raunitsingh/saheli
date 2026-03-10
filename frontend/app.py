import streamlit as st
import requests
import time
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Saheli — AI Field Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp, .main { background-color: #f2ede6 !important; }

.main .block-container {
    padding: 2.8rem 3.2rem 6rem !important;
    max-width: 1080px !important;
}

/* ─── SIDEBAR ─────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #152d22 0%, #1e3d2d 60%, #24472f 100%) !important;
    min-width: 250px !important;
    max-width: 250px !important;
    border-right: none !important;
    box-shadow: 3px 0 20px rgba(0,0,0,0.18) !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 2.2rem 1.3rem 2rem !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: rgba(255,255,255,0.88) !important;
    font-family: 'Inter', sans-serif !important;
}
section[data-testid="stSidebar"] .stRadio > div {
    gap: 5px !important;
    display: flex !important;
    flex-direction: column !important;
}
section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 11px !important;
    padding: 11px 16px !important;
    display: block !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: background 0.18s !important;
    border: 1px solid transparent !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.13) !important;
    border-color: rgba(255,255,255,0.08) !important;
}
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    display: none !important;
}

/* ─── GLOBAL TEXT ─────────────────────────────── */
h1,h2,h3,h4,h5,h6,p,span,div,label,li {
    font-family: 'Inter', sans-serif !important;
}

/* ─── BUTTONS ─────────────────────────────────── */
.stButton > button {
    background: #2d6a4f !important;
    color: #fff !important;
    border: none !important;
    border-radius: 11px !important;
    padding: 13px 26px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 3px 12px rgba(45,106,79,0.28) !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #3a7d5e !important;
    box-shadow: 0 5px 18px rgba(45,106,79,0.38) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ─── FORM INPUTS ─────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #ddd6cc !important;
    font-family: 'Inter', sans-serif !important;
    background: #fff !important;
    font-size: 0.9rem !important;
    color: #1a1a1a !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #2d6a4f !important;
    box-shadow: 0 0 0 3px rgba(45,106,79,0.12) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
    margin-bottom: 5px !important;
}

/* ─── EXPANDERS ───────────────────────────────── */
details {
    background: #fff !important;
    border: 1px solid #e4ddd4 !important;
    border-radius: 14px !important;
    margin-bottom: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05) !important;
}
details summary {
    padding: 16px 20px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    color: #1a1a1a !important;
    cursor: pointer !important;
}
details[open] summary {
    border-bottom: 1px solid #f0ebe4 !important;
}

/* ─── ALERTS ──────────────────────────────────── */
.stSuccess > div, .stWarning > div, .stError > div {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ─── SELECTBOX ───────────────────────────────── */
.stSelectbox [data-baseweb="select"] > div {
    border-radius: 10px !important;
    border: 1.5px solid #ddd6cc !important;
    background: #fff !important;
}

/* ─── HIDE STREAMLIT CHROME ───────────────────── */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── MOCK DATA ─────────────────────────────────────────────────────────────────
MOCK_VISITS = [
    {
        "id": 1, "name": "Radha Devi", "age": 34, "village": "Rampur",
        "date": "2025-03-07", "risk": "high",
        "soap": {
            "subjective": "Patient reports persistent cough for 3 weeks, night sweats, and significant weight loss of approximately 4kg. Fatigue throughout the day. Symptoms began gradually over last month.",
            "objective": "Cough present and productive. Night sweats reported. Visible weight loss noted. No fever recorded at time of visit. No stethoscope available for auscultation.",
            "assessment": "Symptom cluster strongly suggestive of pulmonary tuberculosis — chronic cough >2 weeks combined with night sweats and unexplained weight loss. Immediate referral warranted.",
            "plan": "Refer to nearest PHC within 24 hours for sputum AFB test and chest X-ray. Advise patient to cover mouth while coughing. Inform household contacts of potential exposure.",
        },
        "risk_reason": "TB red flag: cough >2 weeks + night sweats + unexplained weight loss",
        "symptoms": ["persistent cough", "night sweats", "weight loss", "fatigue"],
    },
    {
        "id": 2, "name": "Sunita Kumari", "age": 28, "village": "Baghpat",
        "date": "2025-03-06", "risk": "medium",
        "soap": {
            "subjective": "Patient complains of fever for 3 days, body ache, and mild headache. Fever reported to be high in the evenings. No vomiting. Appetite reduced.",
            "objective": "High-grade fever with evening spike pattern. No rash or bleeding from any site. No breathlessness. Abdomen non-tender.",
            "assessment": "Evening fever spike with body ache raises concern for dengue or malaria. Vector-borne illness screening recommended urgently.",
            "plan": "Refer for RDT malaria test and dengue NS1 antigen test at PHC. Advised to use mosquito nets, take ORS for hydration, and paracetamol for fever.",
        },
        "risk_reason": "Evening fever spike pattern — possible vector-borne illness",
        "symptoms": ["high fever", "body ache", "headache"],
    },
    {
        "id": 3, "name": "Meena Bai", "age": 52, "village": "Rampur",
        "date": "2025-03-05", "risk": "low",
        "soap": {
            "subjective": "Patient reports mild cold and sore throat for 2 days. No fever. Able to eat and drink normally. No breathlessness.",
            "objective": "No fever, no breathing difficulty. Eating and drinking normally. Mild throat irritation on self-report. No skin rash.",
            "assessment": "Symptoms consistent with common upper respiratory tract infection. No red flags present. No referral required at this time.",
            "plan": "Home management advised. Warm saline gargles twice daily, adequate rest, increased fluid intake. Return if fever develops or symptoms worsen after 5 days.",
        },
        "risk_reason": "No red flags — mild URTI, home management sufficient",
        "symptoms": ["cold", "sore throat"],
    },
]

DEMO_CONVERSATION = [
    ("ai",      "नमस्ते। मैं साहेली हूँ। आज आपकी क्या तकलीफ है?"),
    ("patient", "मुझे तीन हफ्ते से खांसी आ रही है और रात को बहुत पसीना होता है।"),
    ("ai",      "खांसी में कुछ आता है? बलगम या कभी खून?"),
    ("patient", "हाँ, थोड़ा बलगम आता है। खून नहीं आया अभी तक।"),
    ("ai",      "पिछले एक-दो महीने में वजन कम हुआ है क्या?"),
    ("patient", "हाँ दीदी, शायद 3-4 किलो कम हो गया है।"),
    ("ai",      "समझ गई। यह गंभीर हो सकता है। आपको आज ही PHC जाना चाहिए।"),
]

# ── HELPERS ───────────────────────────────────────────────────────────────────
RISK_CFG = {
    "high":   {"icon": "🔴", "label": "High Risk",   "bg": "#fef2f2", "color": "#dc2626", "border": "#fca5a5", "banner_bg": "#fff5f5", "banner_border": "#f87171"},
    "medium": {"icon": "🟡", "label": "Medium Risk", "bg": "#fffbeb", "color": "#d97706", "border": "#fde68a", "banner_bg": "#fffbf0", "banner_border": "#fbbf24"},
    "low":    {"icon": "🟢", "label": "Low Risk",    "bg": "#f0fdf4", "color": "#16a34a", "border": "#86efac", "banner_bg": "#f0fdf4", "banner_border": "#4ade80"},
}
SOAP_META = [
    ("S", "Subjective",  "subjective", "#dbeafe", "#1e40af"),
    ("O", "Objective",   "objective",  "#dcfce7", "#166534"),
    ("A", "Assessment",  "assessment", "#fef9c3", "#854d0e"),
    ("P", "Plan",        "plan",       "#ede9fe", "#5b21b6"),
]
RISK_TITLES = {
    "high":   "HIGH RISK — Immediate Referral Required",
    "medium": "MEDIUM RISK — PHC Visit Within 48 Hours",
    "low":    "LOW RISK — Home Management Advised",
}

def badge(level):
    c = RISK_CFG.get(level, RISK_CFG["low"])
    return (f'<span style="background:{c["bg"]};color:{c["color"]};border:1.5px solid {c["border"]};'
            f'border-radius:999px;padding:5px 15px;font-size:0.77rem;font-weight:700;'
            f'font-family:Inter,sans-serif;letter-spacing:0.2px;">{c["icon"]} {c["label"]}</span>')

def fetch_visits():
    try:
        r = requests.get(f"{API_BASE}/visits", timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data:
                return data
    except Exception:
        pass
    return MOCK_VISITS

def page_header(title, subtitle):
    st.markdown(f"""
    <div style="margin-bottom:2.2rem;">
        <div style="font-family:'Playfair Display',serif;font-size:2.1rem;
                    color:#162d22;font-weight:700;line-height:1.15;">{title}</div>
        <div style="font-size:0.85rem;color:#6b7280;margin-top:5px;
                    font-family:'Inter',sans-serif;font-weight:400;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def section_title(text):
    st.markdown(f"""
    <div style="font-family:'Playfair Display',serif;font-size:1.25rem;
                color:#162d22;font-weight:700;margin-bottom:14px;">{text}</div>
    """, unsafe_allow_html=True)

def white_card(html, extra=""):
    return f"""<div style="background:#fff;border:1px solid #e4ddd4;border-radius:15px;
    padding:22px 26px;margin-bottom:14px;box-shadow:0 1px 8px rgba(0,0,0,0.05);{extra}">{html}</div>"""

def soap_card(letter, label, content, bg, color):
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e4ddd4;border-radius:14px;
                padding:20px 24px;margin-bottom:12px;box-shadow:0 1px 8px rgba(0,0,0,0.04);">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <div style="background:{bg};color:{color};border-radius:7px;
                        padding:3px 12px;font-family:'Inter',sans-serif;
                        font-size:0.72rem;font-weight:700;letter-spacing:0.6px;">
                {letter} — {label.upper()}
            </div>
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.92rem;
                    color:#27272a;line-height:1.8;">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def risk_banner(level, reason):
    c = RISK_CFG.get(level, RISK_CFG["low"])
    st.markdown(f"""
    <div style="background:{c['banner_bg']};border:2px solid {c['banner_border']};
                border-radius:14px;padding:18px 22px;margin-bottom:20px;">
        <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1rem;
                    color:#111827;margin-bottom:5px;">
            {c['icon']} {RISK_TITLES.get(level,'')}
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.85rem;color:#6b7280;">
            {reason}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0 4px 22px;border-bottom:1px solid rgba(255,255,255,0.1);margin-bottom:22px;">
        <div style="font-family:'Playfair Display',serif;font-size:2rem;
                    color:#fff;font-weight:700;line-height:1.1;">🌿 Saheli</div>
        <div style="font-size:0.68rem;color:rgba(255,255,255,0.42);text-transform:uppercase;
                    letter-spacing:1.8px;margin-top:6px;">AI Field Companion</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("nav", [
        "🏠  Dashboard",
        "🎙️  New Visit",
        "📋  Visit Records",
        "ℹ️  About",
    ], label_visibility="collapsed")

    st.markdown("""
    <div style="margin-top:36px;background:rgba(255,255,255,0.07);
                border-radius:13px;padding:15px 17px;
                border:1px solid rgba(255,255,255,0.08);">
        <div style="font-size:0.67rem;color:rgba(255,255,255,0.38);
                    text-transform:uppercase;letter-spacing:1.2px;margin-bottom:8px;">Logged in as</div>
        <div style="font-size:0.95rem;color:#fff;font-weight:600;margin-bottom:3px;">Priya Sharma</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.48);">Block Rampur · Uttar Pradesh</div>
    </div>
    <div style="margin-top:16px;background:rgba(74,222,128,0.08);
                border-radius:10px;padding:10px 14px;
                border:1px solid rgba(74,222,128,0.15);">
        <div style="font-size:0.75rem;color:rgba(74,222,128,0.9);font-weight:600;">
            ● Backend Connected
        </div>
        <div style="font-size:0.7rem;color:rgba(255,255,255,0.35);margin-top:2px;">127.0.0.1:8000</div>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# DASHBOARD
# ═════════════════════════════════════════════════════════════════
if page == "🏠  Dashboard":

    now = datetime.now().strftime("%A, %d %B %Y")
    page_header(f"Good afternoon, Priya 👋", f"{now}  ·  Block Rampur, Uttar Pradesh")

    visits     = fetch_visits()
    high_count = sum(1 for v in visits if v.get("risk") == "high")

    # ── Stat cards ──
    c1, c2, c3, c4 = st.columns(4)
    for col, num, label, accent, light in [
        (c1, len(visits),  "Total Visits",  "#2d6a4f", "#d8f3dc"),
        (c2, high_count,   "High Risk",     "#dc2626", "#fee2e2"),
        (c3, "6",          "Referrals",     "#d97706", "#fef3c7"),
        (c4, "14",         "This Month",    "#7c3aed", "#ede9fe"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e4ddd4;border-radius:16px;
                        padding:22px 22px 20px;box-shadow:0 1px 8px rgba(0,0,0,0.05);">
                <div style="width:36px;height:36px;background:{light};border-radius:10px;
                            display:flex;align-items:center;justify-content:center;
                            margin-bottom:12px;">
                    <div style="width:14px;height:14px;background:{accent};border-radius:4px;"></div>
                </div>
                <div style="font-family:'Playfair Display',serif;font-size:2.3rem;
                            color:{accent};line-height:1;font-weight:700;">{num}</div>
                <div style="font-size:0.74rem;color:#9ca3af;margin-top:6px;
                            text-transform:uppercase;letter-spacing:0.8px;
                            font-weight:600;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    # ── Visits list + quick action ──
    left, right = st.columns([2, 1])

    with left:
        section_title("Recent Visits")
        for v in visits[:4]:
            syms = ", ".join(v.get("symptoms", [])[:2])
            c = RISK_CFG.get(v["risk"], RISK_CFG["low"])
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e4ddd4;
                        border-left:4px solid {c['border']};border-radius:14px;
                        padding:16px 20px;margin-bottom:11px;
                        box-shadow:0 1px 6px rgba(0,0,0,0.04);
                        display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-family:'Inter',sans-serif;font-weight:600;
                                font-size:0.97rem;color:#111827;">
                        {v['name']}
                        <span style="color:#9ca3af;font-weight:400;">, {v['age']}y · {v['village']}</span>
                    </div>
                    <div style="font-size:0.78rem;color:#9ca3af;margin-top:4px;
                                font-family:'Inter',sans-serif;">
                        📅 {v['date']}  ·  {syms}
                    </div>
                </div>
                {badge(v['risk'])}
            </div>
            """, unsafe_allow_html=True)

    with right:
        section_title("Quick Actions")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("🎙️  Start New Visit"):
            st.session_state["visit_step"] = 1
            st.rerun()
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("📋  View All Records"):
            st.rerun()

        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e4ddd4;border-radius:14px;
                    padding:18px 20px;margin-top:16px;box-shadow:0 1px 6px rgba(0,0,0,0.04);">
            <div style="font-size:0.72rem;color:#9ca3af;text-transform:uppercase;
                        letter-spacing:0.8px;margin-bottom:10px;font-weight:600;">Today at a Glance</div>
            <div style="font-size:0.88rem;color:#374151;margin-bottom:7px;">
                🏘️  3 villages covered
            </div>
            <div style="font-size:0.88rem;color:#374151;margin-bottom:7px;">
                ⏱️  Avg visit: 12 min
            </div>
            <div style="font-size:0.88rem;color:#374151;">
                📡  Sarvam AI: Online
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# NEW VISIT
# ═════════════════════════════════════════════════════════════════
elif page == "🎙️  New Visit":

    page_header("New Patient Visit", "Voice-powered AI clinical interview in your language")

    step = st.session_state.get("visit_step", 1)

    # ── Progress bar ──
    step_labels = ["Patient Details", "Voice Interview", "SOAP Summary"]
    cols = st.columns(3)
    for i, (col, label) in enumerate(zip(cols, step_labels), 1):
        done   = i < step
        active = i == step
        if active:
            bg, color, border = "#2d6a4f", "#fff", "#2d6a4f"
        elif done:
            bg, color, border = "#d8f3dc", "#2d6a4f", "#74c69d"
        else:
            bg, color, border = "#f2ede6", "#9ca3af", "#e4ddd4"
        with col:
            st.markdown(f"""
            <div style="background:{bg};border:1.5px solid {border};border-radius:12px;
                        padding:12px;text-align:center;">
                <span style="font-family:'Inter',sans-serif;font-size:0.82rem;
                             font-weight:600;color:{color};">
                    {'✓  ' if done else f'{i}.  '}{label}
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ─── STEP 1: Patient Details ───────────────────────────────
    if step == 1:
        section_title("Patient Details")
        with st.form("patient_form"):
            c1, c2 = st.columns(2)
            name   = c1.text_input("Patient Name *", placeholder="e.g. Radha Devi")
            age    = c2.number_input("Age *", min_value=1, max_value=120, value=30)
            c3, c4 = st.columns(2)
            village = c3.text_input("Village *", placeholder="e.g. Rampur")
            gender  = c4.selectbox("Gender", ["Female", "Male", "Other"])
            phone   = st.text_input("📱 Phone Number (for SMS summary)", placeholder="e.g. 9876543210")

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Start Voice Interview →")
            if submitted:
                if name and village:
                    st.session_state.update({
                        "visit_step": 2, "patient_name": name,
                        "patient_age": age, "patient_village": village,
                        "patient_phone": phone,
                    })
                    st.rerun()
                else:
                    st.error("Please fill in Patient Name and Village.")

    # ─── STEP 2: Voice Interview ───────────────────────────────
    elif step == 2:
        name = st.session_state.get("patient_name", "Patient")
        section_title(f"Interview · {name}")

        # Recording pill
        st.markdown("""
        <div style="display:inline-flex;align-items:center;gap:10px;
                    background:#fff0f0;border:1.5px solid #fca5a5;
                    border-radius:999px;padding:8px 20px;margin-bottom:20px;">
            <div style="width:9px;height:9px;background:#dc2626;border-radius:50%;"></div>
            <span style="font-family:'Inter',sans-serif;font-size:0.83rem;
                         color:#dc2626;font-weight:600;letter-spacing:0.3px;">
                RECORDING IN PROGRESS
            </span>
            <span style="font-family:'Inter',sans-serif;font-size:0.78rem;
                         color:#9ca3af;margin-left:8px;">Hindi · English · Regional</span>
        </div>
        """, unsafe_allow_html=True)

        # Chat window
        st.markdown("""
        <div style="background:#fff;border:1px solid #e4ddd4;border-radius:18px;
                    padding:24px;margin-bottom:20px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        """, unsafe_allow_html=True)

        for speaker, text in DEMO_CONVERSATION:
            if speaker == "ai":
                st.markdown(f"""
                <div style="display:flex;gap:10px;margin-bottom:16px;align-items:flex-start;">
                    <div style="width:34px;height:34px;min-width:34px;background:#2d6a4f;
                                border-radius:50%;display:flex;align-items:center;
                                justify-content:center;font-size:0.9rem;">🤖</div>
                    <div style="background:#f0fdf4;border:1px solid #bbf7d0;
                                border-radius:4px 16px 16px 16px;padding:12px 16px;
                                max-width:68%;font-family:'Inter',sans-serif;
                                font-size:0.9rem;color:#1a1a1a;line-height:1.6;">
                        {text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;gap:10px;margin-bottom:16px;
                            justify-content:flex-end;align-items:flex-start;">
                    <div style="background:#1c3d2f;border-radius:16px 4px 16px 16px;
                                padding:12px 16px;max-width:68%;font-family:'Inter',sans-serif;
                                font-size:0.9rem;color:#f0fdf4;line-height:1.6;">
                        {text}
                    </div>
                    <div style="width:34px;height:34px;min-width:34px;background:#e4ddd4;
                                border-radius:50%;display:flex;align-items:center;
                                justify-content:center;font-size:0.9rem;">👤</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏹️  End Interview & Generate SOAP"):
                with st.spinner("🧠 Running AI clinical analysis..."):
                    payload = {
                        "name":    st.session_state.get("patient_name"),
                        "age":     st.session_state.get("patient_age"),
                        "village": st.session_state.get("patient_village"),
                    }
                    try:
                        res = requests.post(f"{API_BASE}/run-visit", json=payload, timeout=60)
                        if res.status_code == 200:
                            st.session_state["visit_result"] = res.json()
                        else:
                            st.session_state["visit_result"] = None
                    except Exception:
                        st.session_state["visit_result"] = None
                    st.session_state["visit_step"] = 3
                st.rerun()
        with col2:
            if st.button("← Back to Details"):
                st.session_state["visit_step"] = 1
                st.rerun()

    # ─── STEP 3: SOAP Summary ──────────────────────────────────
    elif step == 3:
        name  = st.session_state.get("patient_name", "Patient")
        visit = st.session_state.get("visit_result") or MOCK_VISITS[0]
        risk  = visit.get("risk", "high")
        soap  = visit.get("soap", {})

        section_title(f"Visit Summary · {name}")
        st.markdown("""
        <div style="font-size:0.83rem;color:#6b7280;margin-top:-10px;margin-bottom:20px;
                    font-family:'Inter',sans-serif;">
            AI-generated clinical note — review and confirm before saving
        </div>
        """, unsafe_allow_html=True)

        risk_banner(risk, visit.get("risk_reason", ""))

        for letter, label, key, bg, color in SOAP_META:
            soap_card(letter, label, soap.get(key, "—"), bg, color)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("💾  Save to Dashboard"):
                try:
                    requests.post(f"{API_BASE}/save-visit", json=visit, timeout=5)
                except Exception:
                    pass
                st.success("✅ Visit saved!")
                time.sleep(1)
                st.session_state["visit_step"] = 1

        with c2:
            if st.button("📱  Send SMS to Patient"):
                phone = st.session_state.get("patient_phone", "")
                if phone:
                    try:
                        requests.post(f"{API_BASE}/send-sms",
                            json={"phone": phone, "message": str(soap)}, timeout=5)
                        st.success(f"✅ SMS sent to {phone}!")
                    except Exception:
                        st.warning("SMS service unavailable")
                else:
                    st.warning("No phone number was entered.")

        with c3:
            if st.button("🔄  New Visit"):
                st.session_state["visit_step"] = 1
                st.rerun()

# ═════════════════════════════════════════════════════════════════
# VISIT RECORDS
# ═════════════════════════════════════════════════════════════════
elif page == "📋  Visit Records":

    page_header("Visit Records", "All household health cards · Block Rampur, UP")

    col_filter, col_search = st.columns([1, 2])
    with col_filter:
        risk_filter = st.selectbox("Filter by risk", ["All", "High", "Medium", "Low"])
    with col_search:
        search = st.text_input("Search patient name or village", placeholder="e.g. Radha or Rampur")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    visits = fetch_visits()
    shown  = 0
    for v in visits:
        if risk_filter != "All" and v["risk"] != risk_filter.lower():
            continue
        if search and search.lower() not in v["name"].lower() and search.lower() not in v["village"].lower():
            continue
        shown += 1
        c = RISK_CFG.get(v["risk"], RISK_CFG["low"])
        syms = ", ".join(v.get("symptoms", []))

        with st.expander(f"  {v['name']}, {v['age']}y  ·  {v['village']}  ·  {v['date']}"):
            top, _ = st.columns([3, 1])
            with top:
                st.markdown(badge(v["risk"]) + f"""
                <span style="font-family:'Inter',sans-serif;font-size:0.8rem;
                             color:#9ca3af;margin-left:12px;">🩺 {syms}</span>
                """, unsafe_allow_html=True)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            risk_banner(v["risk"], v["risk_reason"])
            for letter, label, key, bg, color in SOAP_META:
                soap_card(letter, label, v["soap"].get(key, "—"), bg, color)

    if shown == 0:
        st.markdown("""
        <div style="text-align:center;padding:48px;background:#fff;
                    border:1px solid #e4ddd4;border-radius:16px;color:#9ca3af;
                    font-family:'Inter',sans-serif;">
            No records match your filter.
        </div>
        """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# ABOUT
# ═════════════════════════════════════════════════════════════════
elif page == "ℹ️  About":

    page_header("About Saheli", "AI Field Companion for India's Community Health Workers")

    left, right = st.columns([3, 2])

    with left:
        for title, content in [
            ("What is Saheli?",
             "Saheli is a voice-based AI clinical co-pilot built for India's 1 million+ ASHA workers. "
             "It conducts structured multilingual health interviews, generates SOAP notes automatically, "
             "and flags high-risk patients for immediate PHC referral — from a basic Android phone, "
             "even without internet."),
            ("Why it matters",
             "India has 1 million ASHA workers visiting rural homes every single day with zero AI support. "
             "Critical conditions — TB, maternal complications, childhood malnutrition — go undetected "
             "not because nobody visited, but because the visit wasn't structured enough to catch them. "
             "Saheli fixes that."),
        ]:
            st.markdown(white_card(f"""
                <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:1.1px;color:#40916c;margin-bottom:10px;
                            font-family:'Inter',sans-serif;">{title}</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.92rem;
                            color:#374151;line-height:1.85;">{content}</div>
            """), unsafe_allow_html=True)

    with right:
        st.markdown(white_card(f"""
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:1.1px;color:#40916c;margin-bottom:14px;
                        font-family:'Inter',sans-serif;">Technology Stack</div>
            {"".join([
                f'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:14px;">'
                f'<div style="font-size:1.1rem;margin-top:1px;">{icon}</div>'
                f'<div><div style="font-family:Inter,sans-serif;font-size:0.83rem;font-weight:600;'
                f'color:#111827;">{name}</div>'
                f'<div style="font-family:Inter,sans-serif;font-size:0.78rem;color:#9ca3af;'
                f'margin-top:2px;">{desc}</div></div></div>'
                for icon, name, desc in [
                    ("🎙️", "Sarvam AI", "10+ Indian languages, codemix STT/TTS"),
                    ("🧠", "Groq LLaMA 3.3 70B", "Clinical interview & symptom extraction"),
                    ("📚", "RAG Pipeline", "ICMR NHM + WHO community health guidelines"),
                    ("🗄️", "Supabase", "Household health records & visit history"),
                    ("📡", "Offline-first", "Whisper fallback · Edge inference"),
                ]
            ])}
        """), unsafe_allow_html=True)
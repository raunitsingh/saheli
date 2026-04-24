# 🌿 Saheli — AI Field Companion for Community Health Workers

<p align="center">
  <img src="https://img.shields.io/badge/Status-In%20Development-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/AI-Groq%20%7C%20Gemini-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Voice-Sarvam%20AI-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Built%20For-Rural%20India-green?style=for-the-badge" />
</p>

<p align="center">
  <strong>Empowering India's 1 million+ ASHA workers with an AI-powered clinical co-pilot that speaks every patient's language.</strong>
</p>

---

## 🩺 The Problem

India's last-mile healthcare runs on **ASHA (Accredited Social Health Activist) workers** — community health volunteers who conduct household screenings across rural India with minimal clinical training and zero digital support.

Every day, critical conditions go undetected — not because no one visited, but because the visit wasn't structured enough to catch them.

| Challenge | Reality |
|-----------|---------|
| 🗂️ Documentation | Paper-based, inconsistent, lost in transit |
| 🌐 Language | 20+ regional languages, no single tool supports them |
| 🧠 Clinical knowledge gap | Limited training means missed red flags |
| 📡 Connectivity | Rural areas have poor or no internet |
| 🔁 Referral chain | Doctors receive patients with zero prior context |

---

## 💡 The Solution — Saheli

**Saheli** (meaning *female companion* in Hindi) is a voice-first AI field companion that sits in the ASHA worker's pocket during every home visit.

It listens to the patient conversation in their local language, guides the ASHA worker through the right clinical questions in real time, and generates a structured health record and referral document — all before she leaves the door.

```
Patient speaks (Hindi / regional language)
        ↓
Sarvam AI — Speech to Text (codemix support)
        ↓
Groq LLM — Structured symptom extraction
        ↓
RAG pipeline — ICMR / NHM guideline grounding
        ↓
SOAP Note + Referral Risk Score generated
        ↓
Synced to PHC doctor before patient arrives
```

---

## ✨ Key Features

- 🎙️ **Voice-first interface** — patients speak naturally, no typing needed
- 🗣️ **Regional language support** — Hindi, Marathi, Tamil, Bhojpuri and more via Sarvam AI
- 🧭 **Real-time guided prompting** — Saheli tells the ASHA worker what to ask next
- 📋 **Automatic SOAP note generation** — structured clinical summary at end of every visit
- 🚨 **Referral risk scoring** — flags high-risk patients with specific recommended action
- 📴 **Offline-first architecture** — core features work without internet, syncs when connected
- 🏠 **Longitudinal household tracking** — health history across multiple visits over time

---

## 🛠️ Tech Stack

### Voice & Language
| Tool | Purpose |
|------|---------|
| [Sarvam AI](https://sarvam.ai) | Regional ASR + TTS — speech to text and text to speech in Indian languages |
| OpenAI Whisper (local) | Offline fallback transcription when no internet |

### AI & Intelligence
| Tool | Purpose |
|------|---------|
| Groq (Llama 3.3 70B) | Fast LLM inference for symptom extraction and interview guidance |
| LangChain / LlamaIndex | RAG orchestration over medical guidelines |
| Sentence Transformers | Embedding generation for vector search |
| FAISS | Local vector similarity search (mobile-optimized) |

### Backend
| Tool | Purpose |
|------|---------|
| Python + FastAPI | Backend inference and API services |
| PostgreSQL + pgvector | Session storage and vector search |
| Supabase | Managed database with offline sync support |

### Frontend
| Tool | Purpose |
|------|---------|
| React + TypeScript | Web interface |
| React Native (planned) | Mobile app for field workers on low-end Android devices |

---

## 📁 Project Structure

```
saheli/
├── backend/
│   ├── api_server.py             # Main FastAPI entry point & API routes
│   ├── app/
│   │   ├── ai/                   # Modular AI agents
│   │   │   ├── clinical_reasoning.py
│   │   │   ├── interview_agent.py
│   │   │   ├── risk_scorer.py
│   │   │   ├── soap_generator.py
│   │   │   └── symptom_extractor.py
│   │   └── interview_pipeline.py # Core conversation state machine
│   ├── database/                 # Supabase client & offline sync queue logic
│   ├── knowledge_base/           # RAG Engine
│   │   ├── docs/                 # ASHA books & WHO guidelines (PDFs)
│   │   ├── vector_db/            # FAISS indexes for lightning-fast retrieval
│   │   └── rag_engine.py         # Document retrieval logic
│   └── voice/                    # Audio processing, Sarvam API & Whisper wrappers
├── frontend/
│   └── app.py                    # Streamlit web dashboard for ASHA workers
├── offline_queue.json            # Local storage payload buffer for offline mode
├── requirement.txt               # Python package dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A virtual environment (recommended)
- API keys for Sarvam AI and Groq

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/saheli.git
cd saheli

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root:

```env
SARVAM_API_KEY=your_sarvam_key_here
GROQ_API_KEY=your_groq_key_here
```

Get your keys from:
- Sarvam AI → [sarvam.ai](https://sarvam.ai)
- Groq → [console.groq.com](https://console.groq.com)

### Run

```bash
# Test speech transcription
python backend/sarvam_stt.py

# Test symptom extraction
python backend/gemini_extract.py

# Start backend server
python backend/main.py
```

---

## 🗺️ Roadmap

- [x] Sarvam AI speech-to-text integration
- [x] LLM-based structured symptom extraction
- [x] Multi-turn clinical interview agent
- [x] RAG pipeline over ICMR/NHM guidelines
- [x] SOAP note generator
- [x] Referral risk scoring engine
- [x] Supabase database integration
- [ ] Offline-first architecture with sync
- [ ] React frontend — ASHA worker UI
- [ ] Household health card and longitudinal tracking
- [ ] React Native mobile app

---

## 🎯 Target Users

**Primary:** ASHA workers conducting rural household health screenings under India's National Health Mission

**Secondary:** PHC (Primary Health Centre) doctors receiving structured referral summaries

---

## 🌍 Why This Matters

> India has over **1 million ASHA workers** visiting rural homes every single day — with no AI support, no structured documentation, and no clinical decision guidance.
>
> Saheli gives every one of them a clinical co-pilot that speaks their patient's language, guides them through the right questions, and hands them a referral document before they leave the door.

This is not another urban health app. This is healthcare infrastructure for the **last mile**.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)

---

## 👨‍💻 Built for ASHA workers working in Rural India

*Saheli was conceived and built to address one of India's most underserved healthcare gaps — the ASHA worker's daily visit.*

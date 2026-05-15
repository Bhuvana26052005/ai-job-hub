# 🤖 AI Career Reputation & Live Job Hub

A cloud-hosted web application built to help job seekers audit their online visibility across large language models, scan resumes for ATS keyword matching, and explore aggregated regional job boards in real-time.

🌐 **Live Demo:https://ai-job-app-gu8bbkpynfhtq5ghguyzrt.streamlit.app/

## 🚀 Core Features
- **AI Identity Visibility Audit:** Uses the Google Gemini API to analyze how recruiters see a profile on public channels.
- **ATS Resume Keyword Scanner:** Scans raw resume text inputs against target job roles to calculate matching scores and missing technical keywords.
- **Dynamic Live Sourcing:** Integrates active RSS data streams to display live jobs directly inside the user interface.
- **Fault-Tolerant Cooldown Engine:** Built-in 10-slot hardcoded fallback database to keep the interface 100% active during external API network constraints (HTTP 429 rate limits).

## 🛠️ Tech Stack
- **Language:** Python 3.12+
- **Framework:** Streamlit (Web UI Dashboard)
- **AI Integration:** Google Generative AI SDK (Gemini 2.5 Flash)
- **Data Protocols:** XML ElementTree parsing, HTTP Requests, URL Component Encoding

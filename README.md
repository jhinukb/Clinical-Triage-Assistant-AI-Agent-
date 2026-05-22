# 🏥 Clinical Triage Assistant — AI Agent

A multi-tool AI agent that classifies patient urgency, suggests differential diagnoses, and assesses abnormal vitals from symptom input. Built with Ollama (Llama 3.2), Streamlit, and real-world data from the OpenFDA API. Deployed via Docker on Railway.

---

## 🔴 Live Demo

👉 **[Try it here](https://clinical-triage-assistant-ai-agent-production.up.railway.app/)**

---

## 🧠 What it does

Most AI chatbots just answer one question at a time. This is an **AI agent** — it thinks, picks the right tool, runs it, and summarises the result in plain English. All in one click.

The agent has 4 medical tools:

| Tool | What it does |
|---|---|
| 🔍 **Symptom Checker** | Takes symptoms → returns top 3 likely conditions with likelihood and next steps |
| 💊 **Drug Interaction Checker** | Flags dangerous medication combinations by severity |
| 📊 **Vitals Assessor** | Identifies abnormal vitals (BP, HR, SpO2, temp) with severity classification |
| 🚨 **Triage Classifier** | Classifies urgency (immediate / urgent / semi-urgent / non-urgent) and recommends care setting |

---

## 🏗️ Architecture

```
User Input (Streamlit UI)
        ↓
Router LLM Call — "which tool should I use?"
        ↓
Tool Runs — returns structured JSON analysis
        ↓
Summariser LLM Call — rewrites in plain English
        ↓
Result displayed with severity indicators
```

Real symptom data is pulled from the **OpenFDA API** to populate the symptom selector with clinically reported terms.

---

## 🛠️ Tech Stack

- **LLM** — Llama 3.2:1b via [Ollama](https://ollama.com) (fully local, no data sent externally)
- **UI** — [Streamlit](https://streamlit.io)
- **Data** — [OpenFDA API](https://open.fda.gov) (real reported adverse event symptoms)
- **Deployment** — Docker + Railway
- **Language** — Python 3.11

---

## 🚀 Run locally

### Prerequisites
- [Ollama](https://ollama.com/download) installed and running
- Python 3.9+

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/jhinukb/Clinical-Triage-Assistant-AI-Agent-.git
cd Clinical-Triage-Assistant-AI-Agent-

# 2. Pull the model
ollama pull llama3.2:1b

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 🐳 Run with Docker

```bash
# Build
docker build -t triage-assistant .

# Run
docker run -p 8501:8501 triage-assistant
```

---

## 📁 Project structure

```
├── app.py                  # Streamlit UI + agent tools
├── AI_Agent_Project.ipynb  # Development notebook with agent walkthrough
├── Dockerfile              # Docker config (installs Ollama + Streamlit)
├── start.sh                # Startup script (runs Ollama + pulls model + starts app)
└── requirements.txt        # Python dependencies
```

---

## 💡 Example queries

**Symptom Checker**
> Patient is a 45-year-old male with persistent cough for 3 weeks, night sweats, and unexplained weight loss

**Drug Interaction**
> Patient is on warfarin and wants to start taking ibuprofen

**Vitals**
> BP 160/100, HR 112 bpm, SpO2 91%, temp 38.8°C, RR 24

**Triage**
> 52-year-old woman, sudden severe headache — worst of her life, stiff neck, sensitive to light

---

## ⚠️ Disclaimer

This tool is for **educational and demonstration purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Never use AI-generated medical outputs to make real clinical decisions.

---

## 👩‍💻 Author

**Jhinuk Barman**
Data Analytics Engineer | UC Davis Cancer Center | UCSF Medical Center

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/jhinukbarman/)
[![GitHub](https://img.shields.io/badge/GitHub-jhinukb-black)](https://github.com/jhinukb)

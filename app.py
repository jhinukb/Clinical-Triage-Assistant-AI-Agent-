import streamlit as st
import ollama
import json
import requests
import pandas as pd

# --- Page config ---
st.set_page_config(page_title="Clinical Triage Assistant", page_icon="🏥", layout="centered")
st.title("Clinical Triage Assistant")
st.caption("Test AI Agent Application by Jhinuk Barman")

# --- Load real symptoms from OpenFDA ---
@st.cache_data
def load_symptoms():
    try:
        url = "https://api.fda.gov/drug/event.json?count=patient.reaction.reactionmeddrapt.exact&limit=50"
        r = requests.get(url, timeout=5)
        data = r.json()
        return [item["term"].title() for item in data["results"]]
    except:
        return ["Fever", "Cough", "Fatigue", "Chest Pain", "Shortness of Breath", "Headache", "Nausea"]

symptoms_list = load_symptoms()

# --- Tools ---
def guess_disease(symptoms):
    response = ollama.chat(model="llama3.2", messages=[{
        "role": "user",
        "content": f"""You are a medical AI assistant.
Given these symptoms: {symptoms}
List the top 3 most likely conditions, each with:
- condition: name
- likelihood: high/medium/low
- matching_symptoms: list
- next_step: recommended action
Reply ONLY with a valid JSON array, no extra text."""
    }])
    return response["message"]["content"]

def triage_patient(description):
    response = ollama.chat(model="llama3.2", messages=[{
        "role": "user",
        "content": f"""Triage this patient: {description}
Return ONLY valid JSON with keys:
- urgency: immediate/urgent/semi-urgent/non-urgent
- reasoning: string
- care_setting: ER/GP/Telehealth/Home care
- red_flags: list of warning signs present"""
    }])
    return response["message"]["content"]

def assess_vitals(vitals):
    response = ollama.chat(model="llama3.2", messages=[{
        "role": "user",
        "content": f"""Assess these vitals: {vitals}
Return ONLY valid JSON array, each item with keys:
- vital, value, status (normal/warning/critical), note"""
    }])
    return response["message"]["content"]

# --- UI ---
tab1, tab2, tab3 = st.tabs(["Symptom Checker", "Vitals Assessor", "Full Triage"])

# Tab 1: Symptom Checker
with tab1:
    st.subheader("Symptom checker")
    selected = st.multiselect("Select symptoms", symptoms_list)
    extra = st.text_input("Any other symptoms not listed?")
    age = st.slider("Patient age", 1, 100, 35)
    sex = st.radio("Sex", ["Male", "Female", "Other"], horizontal=True)

    if st.button("Analyse symptoms", key="sym"):
        all_symptoms = ", ".join(selected) + (f", {extra}" if extra else "")
        query = f"Age {age}, {sex}. Symptoms: {all_symptoms}"

        with st.spinner("Analysing..."):
            raw = guess_disease(query)
            try:
                clean = raw.replace("```json", "").replace("```", "").strip()
                results = json.loads(clean)
                for r in results:
                    color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(r.get("likelihood", "").lower(), "⚪")
                    with st.expander(f"{color} {r.get('condition', 'Unknown')} — {r.get('likelihood', '')} likelihood"):
                        st.write("**Matching symptoms:**", ", ".join(r.get("matching_symptoms", [])))
                        st.write("**Recommended next step:**", r.get("next_step", ""))
            except:
                st.write(raw)

# Tab 2: Vitals Assessor
with tab2:
    st.subheader("Vitals assessor")
    col1, col2 = st.columns(2)
    with col1:
        bp = st.text_input("Blood pressure (e.g. 120/80)")
        hr = st.number_input("Heart rate (bpm)", 30, 250, 75)
        temp = st.number_input("Temperature (°C)", 34.0, 42.0, 37.0, step=0.1)
    with col2:
        spo2 = st.number_input("SpO2 (%)", 50, 100, 98)
        rr = st.number_input("Respiratory rate", 5, 60, 16)

    if st.button("Assess vitals", key="vit"):
        vitals_str = f"BP {bp}, HR {hr}bpm, Temp {temp}°C, SpO2 {spo2}%, RR {rr}"
        with st.spinner("Assessing..."):
            raw = assess_vitals(vitals_str)
            try:
                clean = raw.replace("```json", "").replace("```", "").strip()
                items = json.loads(clean)
                for item in items:
                    status = item.get("status", "normal").lower()
                    color = {"critical": "🔴", "warning": "🟡", "normal": "🟢"}.get(status, "⚪")
                    st.write(f"{color} **{item.get('vital')}** — {item.get('value')} — {item.get('note')}")
            except:
                st.write(raw)

# Tab 3: Full Triage
with tab3:
    st.subheader("Full triage")
    case = st.text_area("Describe the patient case in full", height=150,
                         placeholder="e.g. 52-year-old woman, sudden severe headache, stiff neck, sensitive to light...")

    if st.button("Run triage", key="tri"):
        with st.spinner("Triaging..."):
            raw = triage_patient(case)
            try:
                clean = raw.replace("```json", "").replace("```", "").strip()
                result = json.loads(clean)
                urgency = result.get("urgency", "unknown").upper()
                colors = {"IMMEDIATE": "🔴", "URGENT": "🟠", "SEMI-URGENT": "🟡", "NON-URGENT": "🟢"}
                st.metric("Urgency", f"{colors.get(urgency, '⚪')} {urgency}")
                st.info(f"**Recommended care:** {result.get('care_setting')}")
                st.write("**Reasoning:**", result.get("reasoning"))
                flags = result.get("red_flags", [])
                if flags:
                    st.warning("**Red flags detected:** " + ", ".join(flags))
            except:
                st.write(raw)

st.divider()
st.caption("⚠️ This tool is for educational purposes only and is not a substitute for professional medical advice.")

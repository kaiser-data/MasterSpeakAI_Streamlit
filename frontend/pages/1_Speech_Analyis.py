import streamlit as st
import requests
from dotenv import load_dotenv
import os
from sqlmodel import Session, select
from backend.database import PromptPreset, prompt_engine

load_dotenv()

st.title("\U0001f399\ufe0f Speech Analyzer with GenAI")

speech_text = st.text_area("Paste your speech text here:")
model_choice = st.selectbox("Choose OpenAI Model", ["gpt-3.5-turbo", "gpt-4o"])

with Session(prompt_engine) as session:
    all_prompts = session.exec(select(PromptPreset)).all()
    preset_names = ["Default"] + [p.name for p in all_prompts]
    preset_lookup = {p.name: p for p in all_prompts}

preset_name = st.selectbox("Choose Prompt Preset", preset_names)

if preset_name == "Default":
    system_prompt = "You are an assistant that analyzes speeches. Summarize the speech and identify tone, sentiment, and key themes."
else:
    preset = preset_lookup[preset_name]
    system_prompt = preset.prompt

if st.button("Analyze"):
    if not speech_text.strip():
        st.error("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"content": speech_text, "model": model_choice}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete!")
                    st.markdown("### \U0001f4dd Analysis Result")
                    st.write(result["analysis"])
                else:
                    st.error(f"Backend error ({response.status_code}):")
                    st.json(response.json())
            except Exception as e:
                st.error(f"Request failed: {e}")
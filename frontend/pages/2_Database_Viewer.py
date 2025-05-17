import streamlit as st
from backend.database import SpeechAnalysis, speech_engine
from sqlmodel import Session, select

st.title("\U0001f4be Stored Speech Analyses")

with Session(speech_engine) as session:
    results = session.exec(select(SpeechAnalysis)).all()
    st.write(f"\U0001f4ca Found {len(results)} records in the database.")

    if results:
        for r in results:
            st.markdown(f"### \U0001f194 ID: {r.id}")
            st.markdown(f"**\U0001f9e0 Model Used:** {r.model_used}")
            st.markdown(f"**\U0001f5e3\ufe0f Speech:** {r.content[:100]}...")
            st.markdown(f"**\U0001f4dd Analysis:** {r.analysis_result}")
            st.divider()
    else:
        st.info("No records found in the database.")

# FILE: frontend/pages/3_Prompt_Settings.py
import streamlit as st
from backend.database import PromptPreset, prompt_engine
from sqlmodel import Session, select

st.title("\U0001f527 Prompt Settings")

with Session(prompt_engine) as session:
    presets = session.exec(select(PromptPreset)).all()

    st.subheader("Create a New Prompt Preset")
    name = st.text_input("Preset Name")
    role = st.text_input("Role")
    prompt = st.text_area("Prompt", height=150)

    if st.button("Save Prompt"):
        if name and role and prompt:
            preset = PromptPreset(name=name, role=role, prompt=prompt)
            session.add(preset)
            session.commit()
            st.success("\u2705 Prompt saved successfully.")
        else:
            st.error("Please fill in all fields.")

    st.subheader("\ud83d\udcdc Saved Prompts")
    if presets:
        for p in presets:
            st.markdown(f"**{p.name}** – {p.role}")
            st.markdown(f"`{p.prompt}`")
            st.divider()
    else:
        st.info("No saved prompts.")

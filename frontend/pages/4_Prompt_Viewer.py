import streamlit as st
from sqlmodel import Session, select
from backend.database import PromptPreset, prompt_engine

st.title("📜 Prompt Preset Database")

with Session(prompt_engine) as session:
    prompts = session.exec(select(PromptPreset)).all()

if prompts:
    for p in prompts:
        st.markdown(f"**{p.name}** – {p.role}")
        st.markdown(f"`{p.prompt}`")
        st.divider()
else:
    st.info("No saved prompts.")

import streamlit as st
from sqlmodel import Session, select
from backend.database import PromptPreset, prompt_engine

st.title("🛠️ Prompt Settings")

with Session(prompt_engine) as session:
    presets = session.exec(select(PromptPreset)).all()

    st.subheader("Create a New Prompt Preset")
    name = st.text_input("Preset Name")
    role = st.text_input("Role", placeholder="e.g. 'You are a speech coach'")
    prompt = st.text_area("Prompt", height=150)

    if st.button("Save Prompt"):
        if name and role and prompt:
            preset = PromptPreset(name=name, role=role, prompt=prompt)
            session.add(preset)
            session.commit()
            st.success("✅ Prompt saved successfully.")
        else:
            st.error("Please fill in all fields.")

    st.subheader("📜 Saved Prompts")
    if presets:
        for p in presets:
            st.markdown(f"**{p.name}** – {p.role}")
            st.markdown(f"`{p.prompt}`")
            st.divider()
    else:
        st.info("No saved prompts.")

import streamlit as st
from sqlmodel import Session, select
from backend.database import PromptPreset, prompt_engine

st.title("🛠️ Prompt Settings")

# -- Load all presets
with Session(prompt_engine) as session:
    presets = session.exec(select(PromptPreset)).all()

# -- UI: Create or update a preset
st.subheader("📌 Create or Update Prompt Preset")

preset_names = ["New preset"] + [p.name for p in presets]
selected = st.selectbox("Select a preset to edit", preset_names)

# Default values for new preset
preset_id = None
name = ""
role = ""
prompt = ""

# If existing preset selected, prefill fields
if selected != "New preset":
    selected_preset = next(p for p in presets if p.name == selected)
    preset_id = selected_preset.id
    name = selected_preset.name
    role = selected_preset.role
    prompt = selected_preset.prompt

# Editable fields
name = st.text_input("Preset Name", value=name)
role = st.text_input("Role", value=role, placeholder="e.g. 'You are a speech coach'")
prompt = st.text_area("Prompt", value=prompt, height=150)

if st.button("💾 Save Prompt"):
    if name and role and prompt:
        with Session(prompt_engine) as session:
            if preset_id:  # Update existing
                existing = session.get(PromptPreset, preset_id)
                if existing:
                    existing.name = name
                    existing.role = role
                    existing.prompt = prompt
            else:  # Add new
                new_preset = PromptPreset(name=name, role=role, prompt=prompt)
                session.add(new_preset)
            session.commit()
        st.success("✅ Prompt saved successfully.")
        st.rerun()
    else:
        st.error("Please fill in all fields.")

# -- Display all saved prompts
st.subheader("📜 Saved Prompts")

if presets:
    for p in presets:
        st.markdown(f"**{p.name}** – {p.role}")
        st.markdown(f"`{p.prompt}`")
        st.divider()
else:
    st.info("No saved prompts.")

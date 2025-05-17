import streamlit as st
from sqlmodel import Session, select
from backend.database import PromptPreset, prompt_engine
import pandas as pd

st.title("📜 Prompt Preset Database")

with Session(prompt_engine) as session:
    presets = session.exec(select(PromptPreset)).all()

if not presets:
    st.info("No saved prompts.")
    st.stop()

# Compact table view
df = pd.DataFrame([p.dict() for p in presets])
df_display = df[["id", "name", "role"]].copy()
df_display = df_display.rename(columns={
    "id": "ID",
    "name": "Preset Name",
    "role": "Role"
})

st.dataframe(df_display, use_container_width=True, hide_index=True)

# Dropdown to select and show details
selected_id = st.selectbox("Select a prompt to view details", df["id"])

selected = df[df["id"] == selected_id].iloc[0]
full = df[df["id"] == selected_id].iloc[0].to_dict()

st.subheader(f"🔍 Prompt: {selected['name']}")

with st.expander("View Full Prompt"):
    st.markdown(f"**Role:** `{full['role']}`")
    st.code(presets[selected_id - 1].prompt, language="markdown")

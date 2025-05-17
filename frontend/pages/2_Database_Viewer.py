import streamlit as st
from sqlmodel import Session, select
from backend.database import SpeechAnalysis, speech_engine
import pandas as pd


st.title("💾 Speech Analysis Database")

st.markdown("""
Welcome to the **Speech Analysis DB Viewer**.

- 🧭 Browse recent entries below
- 🔍 Enter an ID to view full speech + GPT analysis
""")

# Load records
with Session(speech_engine) as session:
    records = session.exec(select(SpeechAnalysis).order_by(SpeechAnalysis.id.desc())).all()

if not records:
    st.info("No records found in the database.")
    st.stop()

# Prepare dataframe
df = pd.DataFrame([r.dict() for r in records])
df_display = df[["id", "model_used", "content", "analysis_result"]].copy()
df_display["content"] = df_display["content"].str.slice(0, 60) + "..."
df_display["analysis_result"] = df_display["analysis_result"].str.slice(0, 60) + "..."
df_display = df_display.rename(columns={
    "id": "ID",
    "model_used": "Model",
    "content": "Speech Snippet",
    "analysis_result": "Analysis Snippet"
})

# === Show recent records preview ===
st.markdown("### 📋 Recent Records")
st.dataframe(df_display.head(min(5, len(df_display))), use_container_width=True, hide_index=True)

# === Manual ID selection ===
st.markdown("### 🔍 View Full Record by ID")
id_list = sorted(df["id"].unique(), reverse=True)
manual_id = st.selectbox("Choose Record ID", options=id_list)

# Lookup record
record = df[df["id"] == manual_id]
original = next((r for r in records if r.id == manual_id), None)

if original is None:
    st.error("Could not load the selected record.")
else:
    st.subheader(f"🧾 Record ID: {original.id} — Model: {original.model_used}")

    score_cols = st.columns(3)
    score_cols[0].metric("🧼 Clarity", original.clarity or "-")
    score_cols[1].metric("🧩 Structure", original.structure or "-")
    score_cols[2].metric("🎭 Tone & Engagement", original.tone_engagement or "-")

    st.markdown("### 🗣️ Full Speech")
    st.code(original.content)

    st.markdown("### 🧠 GPT Summary")
    st.write(original.summary or "_No summary available._")

    st.markdown("### 📦 Raw GPT JSON Output")
    st.code(original.analysis_result, language="json")

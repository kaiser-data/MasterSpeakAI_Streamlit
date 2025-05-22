import streamlit as st
from sqlmodel import Session, select
from backend.database import SpeechAnalysis, speech_engine
import pandas as pd

st.title("💾 Speech Analysis Database")

st.markdown("""
Welcome to the **Speech Analysis DB Viewer**.

- 🧭 Browse recent entries below
- 🔍 Scroll through entries using the slider to view full speech + GPT analysis
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

# === Paginated preview of recent records ===
st.markdown("### 📋 Browse Records")

records_per_page = 5
total_pages = (len(df_display) - 1) // records_per_page + 1
page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

start_idx = (page - 1) * records_per_page
end_idx = start_idx + records_per_page

st.dataframe(df_display.iloc[start_idx:end_idx], use_container_width=True, hide_index=True)

# === Slider to select individual record ===
st.markdown("### 🔍 View Full Record by ID")

min_id, max_id = int(df["id"].min()), int(df["id"].max())
selected_id = st.slider("Scroll to Record ID", min_value=min_id, max_value=max_id, value=max_id, step=1)

# Lookup record
record = df[df["id"] == selected_id]
original = next((r for r in records if r.id == selected_id), None)

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

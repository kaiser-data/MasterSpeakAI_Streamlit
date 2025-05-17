import streamlit as st
from sqlmodel import Session, select
from backend.database import SpeechAnalysis, speech_engine
import pandas as pd

st.title("💾 Speech Analysis Database")

st.markdown("""
Welcome to the **Speech Analysis Database**.
You can:
- 🧭 Enter an ID to view the full content and GPT analysis
- 📋 Browse the latest entries in the table below for quick reference
""")

# Load records
with Session(speech_engine) as session:
    records = session.exec(select(SpeechAnalysis).order_by(SpeechAnalysis.id.desc())).all()

if not records:
    st.info("No records found in the database.")
    st.stop()

# Create dataframe
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

# Show up to 5 recent records
st.dataframe(df_display.head(min(5, len(df_display))), use_container_width=True, hide_index=True)

# Manual ID input only
st.subheader("🔍 Enter Record ID to View")

manual_id = st.number_input("Enter an ID", min_value=1, step=1)

# Try to locate the record
record = df_display[df_display["ID"] == manual_id]

if record.empty:
    st.warning(f"No record found with ID {manual_id}")
else:
    selected = record.iloc[0]
    original = next((r for r in records if r.id == manual_id), None)

    if original is None:
        st.error("Could not load the selected record.")
    else:
        st.subheader(f"🧾 Record ID: {manual_id} — Model: {selected['Model']}")

        with st.expander("🗣️ Full Speech Text"):
            st.code(original.content)

        with st.expander("🧠 GPT Analysis Result"):
            st.code(original.analysis_result)

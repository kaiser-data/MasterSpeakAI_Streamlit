import streamlit as st
from sqlmodel import SQLModel, Session, create_engine, select

# Redefine SpeechAnalysis model (same as backend)
class SpeechAnalysis(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    model_used: str
    analysis_result: str

st.title("💾 Stored Speech Analyses")

engine = create_engine("sqlite:///../test.db")

with Session(engine) as session:
    results = session.exec(select(SpeechAnalysis)).all()

    if results:
        for r in results:
            st.markdown(f"### ID: {r.id}")
            st.markdown(f"**Model Used:** {r.model_used}")
            st.markdown(f"**Speech:** {r.content[:100]}...")
            st.markdown(f"**Analysis:** {r.analysis_result}")
            st.divider()
    else:
        st.info("No records found in the database.")
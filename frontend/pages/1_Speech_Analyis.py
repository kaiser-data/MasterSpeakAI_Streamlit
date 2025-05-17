import streamlit as st
import requests
from sqlmodel import SQLModel, Session, create_engine, select

# Load environment variables
from dotenv import load_dotenv
import os

load_dotenv()

# === Sidebar Navigation ===
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["🎙️ Speech Analysis", "💾 View Database"])

# === Page 1: Speech Analysis ===
if page == "🎙️ Speech Analysis":
    st.title("🎙️ Speech Analyzer with GenAI")

    speech_text = st.text_area("Paste your speech text here:")
    model_choice = st.selectbox("Choose OpenAI Model", ["gpt-3.5-turbo", "gpt-4o"])

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
                        st.markdown("### 📝 Analysis Result")
                        st.write(result["analysis"])
                    else:
                        st.error(f"Backend error ({response.status_code}):")
                        st.json(response.json())

                except Exception as e:
                    st.error(f"Request failed: {e}")

# === Page 2: View Database ===
elif page == "💾 View Database":
    st.title("💾 Stored Speech Analyses")

    # Define the same model used by backend
    class SpeechAnalysis(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        content: str
        model_used: str
        analysis_result: str

    # Create engine and session
    engine = create_engine("sqlite:///./test.db")
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
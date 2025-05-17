import streamlit as st
import requests

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
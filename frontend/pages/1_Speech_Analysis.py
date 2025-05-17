import streamlit as st
import requests
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
from sqlmodel import Session, select
from backend.database import PromptPreset, prompt_engine



load_dotenv()

@st.cache_data(ttl=600)
def fetch_available_models():
    try:
        res = requests.get("http://localhost:8000/models")
        if res.ok:
            return res.json()
    except Exception:
        pass
    return ["gpt-3.5-turbo"]  # fallback

# === PAGE TITLE ===
st.title("🎙️ MasterSpeakAI – Speech Analyzer")

# === First row: input left, prompt preset right ===
left, right = st.columns(2)

with left:
    speech_text = st.text_area("📝 Paste your speech here (not code):")


    gpt_models = fetch_available_models()
    model_choice = st.selectbox("🤖 Choose GPT Model", gpt_models, index=0)

with right:
    with Session(prompt_engine) as session:
        all_presets = session.exec(select(PromptPreset)).all()
        preset_names = ["Default"] + [p.name for p in all_presets]
        preset_lookup = {p.name: p for p in all_presets}

    preset_name = st.selectbox("📋 Choose Prompt Preset", preset_names)

    if preset_name == "Default":
        role = "You are a professional speech evaluator."
        prompt_text = (
            "Return JSON with:\n"
            "- clarity (1–10)\n- structure (1–10)\n- tone_engagement (1–10)\n"
            "- summary (1 paragraph)\n\n"
            "If not a speech, set all scores to 0 and explain why."
        )
    else:
        preset = preset_lookup[preset_name]
        role = preset.role
        prompt_text = preset.prompt

    st.markdown(f"**🧾 Preset:** `{preset_name}`")
    st.markdown(f"**🎭 Role:** `{role}`")
    st.code(prompt_text)

# === Submit ===
if st.button("🔍 Analyze Speech"):
    if not speech_text.strip():
        st.error("❗ Please enter speech content.")
    else:
        with st.spinner("Sending to GPT..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"content": speech_text, "model": model_choice}
                )

                if response.status_code != 200:
                    st.error("⚠️ Backend error:")
                    st.json(response.json())
                else:
                    result = response.json()
                    scores = result.get("scores", {})
                    summary = result.get("summary", "")

                    clarity = scores.get("clarity", 0)
                    structure = scores.get("structure", 0)
                    tone = scores.get("tone_engagement", 0)

                    # === Result Layout ===
                    col_chart, col_summary = st.columns(2)

                    with col_chart:
                        st.markdown("### 📊 Evaluation Scores")
                        fig = go.Figure(data=[
                            go.Bar(
                                x=["Clarity", "Structure", "Tone & Engagement"],
                                y=[clarity, structure, tone],
                                text=[clarity, structure, tone],
                                textposition='auto',
                                marker_color=["#636EFA", "#EF553B", "#00CC96"]
                            )
                        ])
                        fig.update_layout(
                            yaxis=dict(range=[0, 10], title="Score"),
                            xaxis=dict(title="Metric"),
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        st.markdown("### 🔢 Score Breakdown")
                        m1, m2, m3 = st.columns(3)
                        m1.metric("🧼 Clarity", clarity)
                        m2.metric("🧩 Structure", structure)
                        m3.metric("🎭 Tone & Engagement", tone)

                    with col_summary:
                        st.markdown("### 🧠 GPT Summary")
                        st.markdown(f"> {summary}" if summary else "_No summary provided._")

                        if summary.lower().startswith("the input does not appear to be"):
                            st.warning("⚠️ GPT flagged this input as not a valid speech.")

            except Exception as e:
                st.error(f"❌ Request failed: {e}")

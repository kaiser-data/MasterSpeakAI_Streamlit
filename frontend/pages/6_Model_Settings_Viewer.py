import streamlit as st
from sqlmodel import Session, select
from backend.database import ModelConfig, model_engine

st.title("🗃️ Model Settings Database")

with Session(model_engine) as session:
    configs = session.exec(select(ModelConfig)).all()

if configs:
    for c in configs:
        st.markdown(f"### **{c.model_name}**")
        st.markdown(f"- Temperature: `{c.temperature}`")
        st.markdown(f"- Max Tokens: `{c.max_tokens}`")
        st.markdown(f"- Top-p: `{c.top_p}`")
        if c.frequency_penalty is not None:
            st.markdown(f"- Frequency Penalty: `{c.frequency_penalty}`")
        if c.presence_penalty is not None:
            st.markdown(f"- Presence Penalty: `{c.presence_penalty}`")
        st.divider()
else:
    st.info("No model settings stored.")

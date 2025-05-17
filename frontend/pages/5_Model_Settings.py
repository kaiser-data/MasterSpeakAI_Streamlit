import streamlit as st
from sqlmodel import Session, select
from backend.database import ModelConfig, model_engine

st.title("🧩 Edit Model Settings")

models = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]

selected_model = st.selectbox("Choose a model", models)

with Session(model_engine) as session:
    config = session.exec(select(ModelConfig).where(ModelConfig.model_name == selected_model)).first()

# Default or load
if config:
    temp = config.temperature or 1.0
    max_tokens = config.max_tokens or 1024
    top_p = config.top_p or 1.0
else:
    temp, max_tokens, top_p = 1.0, 1024, 1.0

temp = st.slider("Temperature", 0.0, 2.0, temp, 0.01)
max_tokens = st.number_input("Max Tokens", min_value=10, max_value=4000, value=max_tokens)
top_p = st.slider("Top-p", 0.0, 1.0, top_p, 0.01)

if st.button("💾 Save Settings"):
    with Session(model_engine) as session:
        if config:
            config.temperature = temp
            config.max_tokens = max_tokens
            config.top_p = top_p
        else:
            config = ModelConfig(
                model_name=selected_model,
                temperature=temp,
                max_tokens=max_tokens,
                top_p=top_p
            )
            session.add(config)
        session.commit()
    st.success("✅ Settings saved!")
    st.rerun()

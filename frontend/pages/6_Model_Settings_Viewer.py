import streamlit as st
from sqlmodel import Session, select
from backend.database import ModelConfig, model_engine
import pandas as pd

st.title("🗃️ Model Settings Database")

# Step 1: Fetch all configs
with Session(model_engine) as session:
    configs = session.exec(select(ModelConfig)).all()

if not configs:
    st.info("No model settings stored.")
    st.stop()

# Step 2: Show in a compact dataframe
df = pd.DataFrame([c.dict() for c in configs])
df_display = df[["id", "model_name", "temperature", "max_tokens", "top_p"]].copy()
df_display = df_display.rename(columns={
    "model_name": "Model",
    "temperature": "Temp",
    "max_tokens": "Max Tokens",
    "top_p": "Top-p"
})

st.dataframe(df_display, use_container_width=True, hide_index=True)

# Step 3: Optional - Select a row and show full detail below
selected_id = st.selectbox("Select a model to view details", df["id"])

selected_config = df[df["id"] == selected_id].iloc[0]

st.subheader(f"🔍 Details for: {selected_config['model_name']}")

with st.expander("View full settings"):
    for key, value in selected_config.items():
        st.markdown(f"**{key}**: `{value}`")

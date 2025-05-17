import streamlit as st

st.set_page_config(page_title="MasterSpeakAI", page_icon="\U0001f9e0")

pg = st.navigation([
    st.Page("pages/0_Home.py", title="Home", icon="\U0001f9e0"),
    st.Page("pages/1_Speech_Analysis.py", title="Speech Analysis", icon="\U0001f399\ufe0f"),
    st.Page("pages/2_Database_Viewer.py", title="View Database", icon="\U0001f4be"),
    st.Page("pages/3_Prompt_Settings.py", title="Prompt Settings", icon="\U0001f527")
])

pg.run()

# FILE: frontend/pages/0_Home.py
import streamlit as st

st.title("\U0001f9e0 MasterSpeakAI – GenAI Speech Analyzer")

st.markdown("""
Welcome to **MasterSpeakAI**, a GenAI-powered speech analysis app powered by:

- \ud83d\udd25 FastAPI (backend)
- \ud83e\udd6a OpenAI GPT Models
- \ud83d\uddc3\ufe0f SQLite Database
- \ud83c\udf9b\ufe0f Streamlit UI

Navigate using the sidebar to:
- \ud83c\udf99\ufe0f Analyze a speech
- \ud83d\udcbe View stored analyses
""")
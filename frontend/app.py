import streamlit as st

st.set_page_config(page_title="MasterSpeakAI", page_icon="🧠")

# Define pages
home_page = st.Page("pages/0_Home.py", title="Home", icon="🧠")
analyze_page = st.Page("pages/1_Speech_Analyis.py", title="Speech Analysis", icon="🎙️")
viewer_page = st.Page("pages/2_Database_Viewer.py", title="View Database", icon="💾")

# Set up navigation
pg = st.navigation([home_page, analyze_page, viewer_page])

# Run the selected page
pg.run()

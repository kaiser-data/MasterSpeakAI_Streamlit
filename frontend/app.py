pg = st.navigation({
    "🧠 MasterSpeakAI": [
        st.Page("pages/0_Home.py", title="Home", icon="🏠"),
    ],
    "🔊 Speech Analysis": [
        st.Page("pages/1_Speech_Analysis.py", title="Analyze Speech", icon="🎙️"),
        st.Page("pages/2_Database_Viewer.py", title="Speech DB Viewer", icon="💾"),
    ],
    "🛠️ Prompt Settings": [
        st.Page("pages/3_Prompt_Settings.py", title="Prompt Editor", icon="🛠️"),
        st.Page("pages/4_Prompt_Viewer.py", title="Prompt DB Viewer", icon="📜"),
    ],
    "⚙️ Model Settings": [
        st.Page("pages/5_Model_Settings.py", title="Edit Model Settings", icon="🧩"),
        st.Page("pages/6_Model_Settings_Viewer.py", title="Model DB Viewer", icon="🗃️"),
    ]
})

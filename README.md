# 🧠 MasterSpeakAI

MasterSpeakAI is a GenAI-powered speech analysis app with:

- 🎛️ A Streamlit frontend using `st.navigation` and `st.Page`
- 🔥 FastAPI backend
- 🧪 GPT-powered analysis (via OpenAI)
- 💾 Local SQLite databases for storing analyses, prompt presets, and model settings
- ⚙️ Model-specific configuration (e.g., temperature, max_tokens)
- 📦 Managed with Poetry

---

## 🚀 Features

- 🎙️ Analyze speech content using OpenAI GPT models (3.5, 4, 4o, etc.)
- 🧠 Create and edit reusable system prompt presets
- ⚙️ Configure model settings (e.g., temperature) per model
- 💾 View and retrieve records using compact scrollable DB viewers
- 📎 Manual ID lookup for speech/prompt/model records
- 🧩 Grouped sidebar navigation for logical app structure

---

## 📁 Project Structure

```

kaiser-data-masterspeakai\_streamlit/
├── backend/
│   ├── database.py              # SQLModel tables for speech, prompts, models
│   ├── main.py                  # FastAPI app with /analyze endpoint
│   ├── init\_db.py               # Creates all DB tables
├── frontend/
│   ├── app.py                   # Main entrypoint with st.navigation sidebar
│   └── pages/
│       ├── 0\_Home.py
│       ├── 1\_Speech\_Analysis.py
│       ├── 2\_Database\_Viewer.py         # Speech DB (manual ID lookup)
│       ├── 3\_Prompt\_Settings.py         # Create/edit prompts
│       ├── 4\_Prompt\_Viewer.py           # Prompt DB (manual ID lookup)
│       ├── 5\_Model\_Settings.py          # Edit model config
│       └── 6\_Model\_Settings\_Viewer.py   # View saved configs
├── init\_db.py                  # Calls backend.init\_db functions
├── pyproject.toml              # Poetry config
├── requirements.txt            # pip fallback
├── speech\_db.db
├── prompt\_db.db
├── model\_settings.db
└── .env                        # For OPENAI\_API\_KEY

````

---

## 🧭 Sidebar Navigation

Organized using `st.navigation()` with icons and sections:

- 🧠 MasterSpeakAI  
  - 🏠 Home

- 🔊 Speech Analysis  
  - 🎙️ Analyze Speech  
  - 💾 Speech DB Viewer (with manual ID input)

- 🛠️ Prompt Settings  
  - 🛠️ Prompt Editor  
  - 📜 Prompt DB Viewer (with manual ID input)

- ⚙️ Model Settings  
  - 🧩 Edit Model Settings (temperature, top_p, etc.)  
  - 🗃️ Model DB Viewer

---

## 📦 Dependency Management with Poetry

> This project uses [Poetry](https://python-poetry.org/) to manage dependencies and virtual environments.

### 📥 Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
````

Ensure it's on your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

### 📦 Install Dependencies

```bash
git clone https://github.com/your-org/kaiser-data-masterspeakai_streamlit.git
cd kaiser-data-masterspeakai_streamlit
poetry install
```

---

### 🐍 Run the App

```bash
poetry run streamlit run frontend/app.py
```

---

## 🔧 Initialize the Databases

```bash
poetry run python init_db.py
```

Creates:

* `speech_db.db`
* `prompt_db.db`
* `model_settings.db`

---

## 🧪 Run Backend API

```bash
poetry run uvicorn backend.main:app --reload
```

Visit the docs at:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Environment Variables

Create a `.env` file with your OpenAI key:

```
OPENAI_API_KEY=your-key-here
```

---

## 🗂️ Future Improvements

* ⏳ User authentication
* ⏳ Role-based prompt/model visibility
* ⏳ Speech-to-text input support
* ⏳ Export results to CSV
* ⏳ Admin edit/delete for DB records

---

## 🪪 License

MIT License.

```


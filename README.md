Absolutely — here’s a clear and polished **`README.md`** that explains your app, its structure, and how to use **Poetry** for managing the environment.

---

## ✅ Recommended `README.md`

```markdown
# 🧠 MasterSpeakAI

MasterSpeakAI is a GenAI-powered speech analysis app with:

- 🎛️ A Streamlit frontend
- 🔥 FastAPI backend
- 🧪 GPT-powered analysis (via OpenAI)
- 💾 SQLite databases for storing analyses and custom prompt presets
- 📦 Managed using Poetry for clean dependency handling

---

## 🚀 Features

- 🎙️ Analyze speeches with GPT models (gpt-3.5-turbo, gpt-4o, etc.)
- 🧠 Customize system prompts to control model behavior
- 📊 View and manage stored analysis history
- ⚙️ Full local database support for both prompts and results

---

## 📁 Project Structure

```

kaiser-data-masterspeakai\_streamlit/
├── backend/                # FastAPI backend
│   ├── database.py
│   └── main.py
├── frontend/               # Streamlit frontend
│   ├── app.py              # Entry point (uses st.navigation)
│   └── pages/              # Multi-page setup
│       ├── 0\_Home.py
│       ├── 1\_Speech\_Analyis.py
│       ├── 2\_Database\_Viewer.py
│       └── 3\_Prompt\_Settings.py
├── speech\_db.db            # Stores speech analysis records
├── prompt\_db.db            # Stores custom prompt presets
├── pyproject.toml          # Poetry configuration
├── requirements.txt        # Optional: for pip fallback
├── init\_db.py              # Script to initialize DBs

````

---

## 📦 Dependency Management with Poetry

> This project uses [Poetry](https://python-poetry.org/) to manage Python packages and virtual environments.

### 📥 Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
````

Make sure it’s on your path:

```bash
export PATH=\"$HOME/.local/bin:$PATH\"
```

---

### 📦 Install Dependencies

Clone the repo and run:

```bash
cd kaiser-data-masterspeakai_streamlit
poetry install
```

---

### 🐍 Activate Environment

With Poetry 2.x+, either run:

```bash
poetry run streamlit run frontend/app.py
```

Or activate the venv directly:

```bash
source $(poetry env info --path)/bin/activate
streamlit run frontend/app.py
```

---

## 🔧 Initialize the Databases

```bash
poetry run python init_db.py
```

This creates:

* `speech_db.db` → for storing analysis results
* `prompt_db.db` → for custom prompt presets

---

## ▶️ Running the App

```bash
poetry run streamlit run frontend/app.py
```

In your browser: `http://localhost:8501`

---

## 🧪 Running the Backend (Optional)

The backend is a FastAPI server:

```bash
poetry run uvicorn backend.main:app --reload
```

Visit `http://localhost:8000/docs` to test the API.

---

## 🔐 Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your-key-here
```

Used by both the backend and test scripts to connect to OpenAI.

---

## 📌 TODO / Future Features

* ✅ Role-based prompt configuration
* ✅ Database-driven prompt management
* ⏳ User login and authentication
* ⏳ Deployment (Streamlit Cloud / Docker)
* ⏳ Speech-to-text input for audio files

---

## 💬 License

MIT License. 

```


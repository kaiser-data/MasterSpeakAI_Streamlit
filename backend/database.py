from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional

# === Speech DB ===
class SpeechAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    model_used: str
    analysis_result: str

speech_engine = create_engine("sqlite:///speech_db.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(speech_engine)

# === Prompt DB ===
class PromptPreset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: str
    prompt: str

prompt_engine = create_engine("sqlite:///prompt_db.db")

def create_prompt_table():
    SQLModel.metadata.create_all(prompt_engine)

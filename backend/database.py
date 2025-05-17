from sqlmodel import Field, SQLModel, create_engine
from typing import Optional

# === Speech DB ===
class SpeechAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    model_used: str
    analysis_result: str  # raw JSON from GPT

    clarity: Optional[int] = None
    structure: Optional[int] = None
    tone_engagement: Optional[int] = None
    summary: Optional[str] = None

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

class ModelConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model_name: str
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None

model_engine = create_engine("sqlite:///model_settings.db")

def create_model_table():
    SQLModel.metadata.create_all(model_engine)



from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional

class SpeechAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    model_used: str
    analysis_result: str

# Create DB engine
engine = create_engine("sqlite:///./test.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
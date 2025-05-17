# backend/schemas.py

from pydantic import BaseModel
from typing import Optional


# === Incoming request to /analyze ===
class AnalyzeRequest(BaseModel):
    content: str
    model: str = "gpt-3.5-turbo"


# === Structured scores returned from analysis ===
class ScoreFields(BaseModel):
    clarity: Optional[int]
    structure: Optional[int]
    tone_engagement: Optional[int]


# === Outgoing response from /analyze ===
class AnalyzeResponse(BaseModel):
    id: int
    scores: ScoreFields
    summary: str


# === Optional: DB read model for listing entries ===
class SpeechAnalysisOut(BaseModel):
    id: int
    content: str
    model_used: str
    clarity: Optional[int]
    structure: Optional[int]
    tone_engagement: Optional[int]
    summary: Optional[str]

    class Config:
        orm_mode = True

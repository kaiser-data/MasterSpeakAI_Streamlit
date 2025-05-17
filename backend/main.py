from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from backend.database import engine, SpeechAnalysis
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class AnalyzeRequest(BaseModel):
    content: str
    model: str = "gpt-3.5-turbo"

@app.post("/analyze")
def analyze_speech(request: AnalyzeRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes speeches. Summarize the speech and identify tone, sentiment, and key themes."},
                {"role": "user", "content": request.content}
            ]
        )
        analysis = response.choices[0].message.content

        with Session(engine) as session:
            db_record = SpeechAnalysis(
                content=request.content,
                model_used=request.model,
                analysis_result=analysis
            )
            session.add(db_record)
            session.commit()
            session.refresh(db_record)

        return {"id": db_record.id, "analysis": analysis}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
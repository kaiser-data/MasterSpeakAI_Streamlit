from fastapi import FastAPI, HTTPException
from sqlmodel import Session
from backend.database import speech_engine, SpeechAnalysis
from backend.schemas import AnalyzeRequest, AnalyzeResponse, ScoreFields
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from fastapi.responses import JSONResponse
from functools import lru_cache

load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_speech(request: AnalyzeRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a speech evaluator. First, determine if the input is a real speech intended for delivery "
                        "to an audience — not code, a prompt, or unrelated text.\n\n"
                        "If the input is not a speech, return:\n"
                        "{\n  \"clarity\": 0,\n  \"structure\": 0,\n  \"tone_engagement\": 0,\n  "
                        "\"summary\": \"The input does not appear to be a valid speech.\"\n}\n\n"
                        "Otherwise, return:\n"
                        "{\n  \"clarity\": <1–10>,\n  \"structure\": <1–10>,\n  "
                        "\"tone_engagement\": <1–10>,\n  \"summary\": \"...\" \n}\n\n"
                        "Respond with JSON only. No markdown, no explanation."
                    )
                },
                {
                    "role": "user",
                    "content": request.content
                }
            ]

        )

        analysis = response.choices[0].message.content
        result = json.loads(analysis)

        with Session(speech_engine) as session:
            db_record = SpeechAnalysis(
                content=request.content,
                model_used=request.model,
                analysis_result=analysis,
                clarity=result.get("clarity"),
                structure=result.get("structure"),
                tone_engagement=result.get("tone_engagement"),
                summary=result.get("summary")
            )
            session.add(db_record)
            session.commit()
            session.refresh(db_record)

        return AnalyzeResponse(
            id=db_record.id,
            scores=ScoreFields(
                clarity=db_record.clarity,
                structure=db_record.structure,
                tone_engagement=db_record.tone_engagement
            ),
            summary=db_record.summary or ""
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
def list_safe_chat_models():
    return JSONResponse(content=[
        "gpt-4o",
        "gpt-4.1",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
        "gpt-4-1106-preview",
        "gpt-3.5-turbo-1106"
    ])

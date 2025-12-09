# backend/app/api/routes/voice.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.voice.stt import transcribe_audio
from app.voice.tts import synthesize_tts
from app.llm.agent import answer_query

router = APIRouter()

@router.post("/ask")
async def voice_ask(file: UploadFile = File(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    """
    Receive audio file -> STT -> LLM -> TTS -> return audio + text
    """
    try:
        audio_bytes = await file.read()
        text = transcribe_audio(audio_bytes)  # implement in voice.stt
        answer, sources = await answer_query(user_id, text, db=db)
        tts_audio = synthesize_tts(answer)    # implement in voice.tts, return bytes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # return audio as base64 or attachment; here we'll return text plus indication
    return {"transcript": text, "answer": answer, "audio_base64": tts_audio}

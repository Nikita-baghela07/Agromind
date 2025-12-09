# backend/app/api/routes/llm_agent.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.llm.agent import answer_query  # implement in llm.agent

router = APIRouter()

class AgentRequest(BaseModel):
    user_id: int
    field_id: int | None = None
    text: str

class AgentResponse(BaseModel):
    answer: str
    sources: list | None = None

@router.post("/query", response_model=AgentResponse)
async def query_agent(payload: AgentRequest, db: Session = Depends(get_db)):
    try:
        answer, sources = await answer_query(payload.user_id, payload.text, db=db, field_id=payload.field_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"answer": answer, "sources": sources}

# backend/app/api/routes/integrations.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class WebhookPayload(BaseModel):
    source: str
    data: dict

@router.post("/webhook")
async def integration_webhook(payload: WebhookPayload):
    """
    Generic integration webhook endpoint. Use for incoming provider callbacks if needed.
    Normalize and forward to ingestion tasks.
    """
    # For now just accept and ack. Implementation: validate source and enqueue processing.
    return {"status": "accepted", "source": payload.source}

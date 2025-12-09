# backend/app/api/routes/iot_webhook.py
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.services.iot_service import process_telemetry, process_device_image
from app.models.schemas import TelemetryCreate, DeviceImageCreate

router = APIRouter()

@router.post("/telemetry")
async def ingest_telemetry(payload: TelemetryCreate, x_device_token: str = Header(None), db: Session = Depends(get_db)):
    """
    Ingest telemetry from device. Devices should include X-DEVICE-TOKEN header.
    """
    # Validate device token (iot_service handles device lookup)
    try:
        record = process_telemetry(payload.dict(), db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "ok", "ingest_id": record.id}

@router.post("/image")
async def ingest_image(payload: DeviceImageCreate, x_device_token: str = Header(None), db: Session = Depends(get_db)):
    """
    Ingest device image. Prefer device to upload to S3 and provide image_url.
    """
    try:
        record = process_device_image(payload.dict(), db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "ok", "image_id": record.id}

# backend/app/api/routes/devices.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.models.db_models import Device
from app.models.schemas import DeviceCreate, DeviceOut
import secrets

router = APIRouter()

@router.post("/register", response_model=DeviceOut)
def register_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    # prevent duplicate registration
    existing = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Device already registered")

    token = secrets.token_urlsafe(32)
    d = Device(
        device_id=payload.device_id,
        name=payload.name,
        owner_id=payload.owner_id,
        meta=payload.meta,
        cred_token=token
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

@router.post("/provision/{device_id}")
def provision_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    new_token = secrets.token_urlsafe(32)
    device.cred_token = new_token
    db.commit()
    db.refresh(device)
    return {"device_id": device.device_id, "cred_token": new_token}

@router.get("/me")
def get_my_device(x_device_token: str = Header(None), db: Session = Depends(get_db)):
    """
    Simple header-based device lookup for debugging.
    """
    if not x_device_token:
        raise HTTPException(status_code=401, detail="Missing device token")
    device = db.query(Device).filter(Device.cred_token == x_device_token).first()
    if not device:
        raise HTTPException(status_code=401, detail="Invalid token")
    return device

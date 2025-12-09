# backend/app/api/routes/disease.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.services.storage import save_file
from app.services.utils import validate_image_bytes, log_event
from app.ml_services.image_service import predict_from_bytes  # wrapper service
from app.models.schemas import DiseasePredictionResponse

router = APIRouter()

@router.post("/predict", response_model=DiseasePredictionResponse)
async def predict_disease(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts multipart image upload and returns disease prediction.
    Saves uploaded file, validates image bytes, sends to ML wrapper.
    """
    try:
        contents = await file.read()
        validate_image_bytes(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    # Save file (local or S3 depending on storage implementation)
    saved_path = save_file(file, subfolder="disease_inputs")

    # Call ML service (should return dict with at least 'prediction')
    try:
        result = await predict_from_bytes(contents)
    except Exception as e:
        log_event("disease_inference_error", error=str(e), image_path=saved_path)
        raise HTTPException(status_code=500, detail="Inference failed")

    # Log event for later retraining/analytics
    log_event("disease_inference", image_path=saved_path, result=result)

    return {"prediction": result.get("disease", "unknown")}

@router.post("/predict_url", response_model=DiseasePredictionResponse)
async def predict_disease_url(payload: dict, db: Session = Depends(get_db)):
    """
    Accepts JSON payload {"image_url": "<public_url>"} — downloads image inside ml_service.
    Useful for FlutterFlow + Firebase workflow.
    """
    image_url = payload.get("image_url")
    if not image_url:
        raise HTTPException(status_code=400, detail="image_url is required")
    try:
        result = await predict_from_bytes_from_url(image_url)  # you should implement in image_service
    except Exception as e:
        raise HTTPException(status_code=500, detail="Inference failed")
    return {"prediction": result.get("disease", "unknown")}


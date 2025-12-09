# backend/app/api/routes/crop_recommendation.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.models.schemas import CropRecommendRequest, CropRecommendResponse
from app.ml_services.crop_service import recommend_crop  # wrapper service
from app.services.utils import validate_crop_inputs, log_event

router = APIRouter()

@router.post("/recommend", response_model=CropRecommendResponse)
async def recommend(request: CropRecommendRequest, db: Session = Depends(get_db)):
    """
    Take soil + weather + basic features and return recommended crop.
    This wrapper validates inputs and calls your crop model service.
    """
    # Validate ranges
    validate_crop_inputs(request.temperature, request.humidity, request.rainfall)

    # The crop_service should accept either the raw features or a normalized dict
    try:
        crop = await recommend_crop(
            soil_type=request.soil_type,
            temperature=request.temperature,
            humidity=request.humidity,
            rainfall=request.rainfall,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log_event("crop_recommendation_error", error=str(e))
        raise HTTPException(status_code=500, detail="Crop recommendation failed")

    log_event("crop_recommendation", soil=request.soil_type, crop=crop)
    return {"recommended_crop": crop}

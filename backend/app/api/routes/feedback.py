from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.models.db_models import Feedback
from app.services.feedback_service import create_feedback, get_all_feedback

router = APIRouter()

# ─────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────
class FeedbackRequest(BaseModel):
    user_id: int
    message: str
    prediction_result: str = None  # optional, attach what user saw

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@router.post("/")
def submit_feedback(data: FeedbackRequest, db: Session = Depends(get_db)):
    feedback = Feedback(
        user_id=data.user_id,
        message=data.message,
        prediction_result=data.prediction_result
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"message": "Feedback submitted successfully", "feedback_id": feedback.id}


@router.get("/")
def list_feedback(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).all()
    return [
        {
            "id": f.id,
            "user_id": f.user_id,
            "message": f.message,
            "prediction_result": f.prediction_result,
            "created_at": f.created_at
        }
        for f in feedbacks
    ]



@router.post("/")
def submit(data: FeedbackRequest, db: Session = Depends(get_db)):
    fb = create_feedback(db, data.user_id, data.message, data.prediction_result)
    return {"message": "Feedback saved", "feedback_id": fb.id}

@router.get("/")
def list_all(db: Session = Depends(get_db)):
    return get_all_feedback(db)

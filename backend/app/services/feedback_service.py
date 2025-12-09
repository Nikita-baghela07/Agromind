from sqlalchemy.orm import Session
from app.models.db_models import Feedback

def create_feedback(db: Session, user_id: int, message: str, prediction_result: str = None):
    feedback = Feedback(
        user_id=user_id,
        message=message,
        prediction_result=prediction_result
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def get_all_feedback(db: Session):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()

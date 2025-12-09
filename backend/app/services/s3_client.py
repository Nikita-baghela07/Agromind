from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.models.db_models import User
from app.core.security import verify_password, create_jwt_token

def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_jwt_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer", "username": user.username}

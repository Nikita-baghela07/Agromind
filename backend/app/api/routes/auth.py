
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.services.database import get_db
from app.models.db_models import User
from app.services.token_service import create_access_token, create_refresh_token, revoke_token, decode_token, is_token_revoked
from app.core.security import get_password_hash, verify_password
from app.models.schemas import TokenResponse  # optional to import your schema

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(username=payload.username, email=payload.email, password_hash=get_password_hash(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created", "user_id": user.id}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    subject = {"user_id": user.id}
    access = create_access_token(subject)
    refresh = create_refresh_token(subject)
    return {
        "access_token": access["token"],
        "access_jti": access["jti"],
        "access_expires": access["expires"].isoformat(),
        "refresh_token": refresh["token"],
        "refresh_jti": refresh["jti"],
        "refresh_expires": refresh["expires"].isoformat(),
        "username": user.username
    }

@router.post("/refresh")
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    try:
        data = decode_token(payload.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    jti = data.get("jti")
    if is_token_revoked(db, jti):
        raise HTTPException(status_code=401, detail="Refresh token revoked")
    if data.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Not a refresh token")
    subject = data.get("sub")
    access = create_access_token(subject)
    return {
        "access_token": access["token"],
        "access_jti": access["jti"],
        "access_expires": access["expires"].isoformat()
    }

@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    """
    Expect client to send refresh token in Authorization header or body (here we check header or JSON).
    We'll revoke that refresh token so it cannot be used again.
    """
    refresh_token = None
    auth = request.headers.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        refresh_token = auth.split(" ", 1)[1].strip()

    if not refresh_token:
        body = {}
        try:
            body = request.json()
            refresh_token = body.get("refresh_token")
        except:
            pass

    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token provided")

    try:
        payload = decode_token(refresh_token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

    jti = payload.get("jti")
    revoke_token(db, jti, token_type=payload.get("type", "refresh"))
    return {"message": "Logged out (refresh token revoked)"}

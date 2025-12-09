
from datetime import datetime, timedelta
import uuid
from typing import Dict, Any, Optional

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.db_models import TokenBlocklist

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_EXPIRE_DAYS = int(getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 30))) \
    if hasattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS") else int(settings.__dict__.get("REFRESH_TOKEN_EXPIRE_DAYS", 30))

# helper to create unique JWT id
def _create_jti() -> str:
    return uuid.uuid4().hex

def create_access_token(subject: Dict[str, Any], expires_minutes: Optional[int] = None) -> Dict[str, Any]:
    jti = _create_jti()
    expire = datetime.utcnow() + timedelta(minutes=(expires_minutes or ACCESS_EXPIRE_MINUTES))
    payload = {
        "jti": jti,
        "exp": expire,
        "type": "access",
        "sub": subject
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token, "jti": jti, "expires": expire}

def create_refresh_token(subject: Dict[str, Any], expires_days: Optional[int] = None) -> Dict[str, Any]:
    jti = _create_jti()
    expire = datetime.utcnow() + timedelta(days=(expires_days or REFRESH_EXPIRE_DAYS))
    payload = {
        "jti": jti,
        "exp": expire,
        "type": "refresh",
        "sub": subject
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token, "jti": jti, "expires": expire}

def revoke_token(db: Session, jti: str, token_type: str = "refresh"):
    """
    Add token jti to blocklist (revoke).
    """
    tb = TokenBlocklist(jti=jti, token_type=token_type)
    db.add(tb)
    db.commit()
    db.refresh(tb)
    return tb

def is_token_revoked(db: Session, jti: str) -> bool:
    """
    Check whether a jti is in the blocklist.
    """
    if not jti:
        return True
    exists = db.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).first()
    return exists is not None

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode token and return payload; raises JWTError on failure.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

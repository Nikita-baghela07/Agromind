# backend/app/api/routes/user.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.services.database import get_db
from app.services import user_service
from app.models.db_models import User as UserModel
from app.models.schemas import UserCreate, UserOut, UserLogin
from app.api.deps import get_current_user

router = APIRouter()

# ----------------------
# Public endpoints
# ----------------------
@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Returns: {"message": "User registered successfully", "user_id": <id>}
    """
    try:
        user = user_service.create_user(db, payload.username, payload.email, payload.password)
    except Exception as e:
        # user_service raises HTTPException for duplicates; re-raise or wrap
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "User registered successfully", "user_id": user.id}


@router.post("/login", response_model=dict)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return an access token.
    Uses user_service.authenticate_user which returns (token, user).
    """
    try:
        token, user = user_service.authenticate_user(db, payload.email, payload.password)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Login successful", "access_token": token, "username": user.username}


# ----------------------
# Protected endpoints
# ----------------------
@router.get("/me", response_model=UserOut)
def read_own_profile(current_user: UserModel = Depends(get_current_user)):
    """
    Returns the profile of the currently authenticated user.
    """
    return current_user


@router.get("/", response_model=List[UserOut])
def list_users(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    List all users.

    NOTE: This endpoint is protected. In a real app you'd check role/permissions and paginate.
    """
    users = db.query(UserModel).all()
    return users


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a specific user by id. Protected.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    username: Optional[str] = Body(None),
    email: Optional[str] = Body(None),
    password: Optional[str] = Body(None),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update user fields (username, email, password). Protected.
    Only allows the user to update their own profile (no role system here).
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if username:
        user.username = username
    if email:
        # Basic uniqueness check
        existing = db.query(UserModel).filter(UserModel.email == email, UserModel.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = email
    if password:
        # delegate hashing to core.security or user_service
        from app.core.security import get_password_hash
        user.password_hash = get_password_hash(password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete a user. Only the user themself can delete their account in this implementation.
    (You can expand to admin-based deletion later.)
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully", "user_id": user_id}


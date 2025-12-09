from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# ─────────────────────────────────────────────
# Base Schemas — common shared properties
# ─────────────────────────────────────────────

class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True  # allows SQLAlchemy models to work with Pydantic


# ─────────────────────────────────────────────
# User Schemas
# ─────────────────────────────────────────────

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase, TimestampMixin):
    id: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: Optional[int] = None
    exp: Optional[int] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


# ─────────────────────────────────────────────
# Feedback Schemas
# ─────────────────────────────────────────────

class FeedbackBase(BaseModel):
    message: str = Field(..., max_length=500)
    prediction_result: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    user_id: int


class FeedbackOut(FeedbackBase, TimestampMixin):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# ─────────────────────────────────────────────
# Disease Prediction Schemas
# ─────────────────────────────────────────────

class DiseasePredictionResponse(BaseModel):
    prediction: str


class DiseaseURLRequest(BaseModel):
    image_url: str = Field(..., description="Publicly accessible image URL")


# ─────────────────────────────────────────────
# Crop Recommendation Schemas (for future use)
# ─────────────────────────────────────────────

class CropRecommendRequest(BaseModel):
    soil_type: str
    temperature: float
    humidity: float
    rainfall: float


class CropRecommendResponse(BaseModel):
    recommended_crop: str

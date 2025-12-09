from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base
from sqlalchemy.types import Float, JSON, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    feedbacks = relationship("Feedback", back_populates="user")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(500))
    prediction_result = Column(String(120))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
    
class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    geojson = Column(JSON)
    area = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketPrice(Base):
    __tablename__ = "market_prices"
    id = Column(Integer, primary_key=True)
    commodity = Column(String)
    market = Column(String)
    price = Column(Float)
    date = Column(DateTime)
    source = Column(String)

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    field_id = Column(Integer, nullable=True)
    model_type = Column(String)
    input_ref = Column(String)  # image path or request id
    output = Column(JSON)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# append to backend/app/models/db_models.py
class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(256), unique=True, index=True)   # JWT ID
    token_type = Column(String(50))                      # "access" or "refresh"
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=True)

    def __repr__(self):
        return f"<TokenBlocklist jti={self.jti} type={self.token_type}>"

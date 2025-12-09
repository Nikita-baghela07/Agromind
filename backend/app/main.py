from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import disease, health, user, feedback
from app.api.routes import disease, health, user, feedback, crop_recommendation
from app.core.middleware import RequestLoggingMiddleware
from app.api.routes import auth
#from app.api.routes import devices, iot_webhook, integrations, llm_agent, voice

from app.api.router import api_router
# ─────────────────────────────────────────────
# Initialize FastAPI App
# ─────────────────────────────────────────────
app = FastAPI(
    title="AgroMind Backend",
    version="1.0.0",
    description="AI-powered Crop Disease Prediction and Recommendation API",
)

# ─────────────────────────────────────────────
# CORS (for FlutterFlow, Streamlit, Web Frontends)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["https://yourdomain.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

# ─────────────────────────────────────────────
# Include API Routers
# ─────────────────────────────────────────────
app.include_router(api_router)


# ─────────────────────────────────────────────
# Root Endpoint
# ─────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "🌿 AgroMind API is running!",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": ["/health", "/disease/predict", "/disease/predict_url"],
    }
    
    


# ─────────────────────────────────────────────
# Run with:
# uvicorn app.main:app --reload
# ─────────────────────────────────────────────

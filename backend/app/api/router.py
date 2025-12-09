# backend/app/api/router.py
from fastapi import APIRouter
from .routes import (
    health,
    disease,
    crop_recommendation,
    user,
    feedback,
    devices,
    iot_webhook,
    integrations,
    llm_agent,
    voice,
)

api_router = APIRouter()

# include specific routers from route modules
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(disease.router, prefix="/disease", tags=["Disease"])
api_router.include_router(crop_recommendation.router, prefix="/crop", tags=["Crop"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
api_router.include_router(devices.router, prefix="/devices", tags=["Devices"])
api_router.include_router(iot_webhook.router, prefix="/iot", tags=["IoT"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])
api_router.include_router(llm_agent.router, prefix="/agent", tags=["LLM Agent"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice"])

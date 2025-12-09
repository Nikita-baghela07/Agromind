# backend/app/api/routes/__init__.py
"""
Import route modules so that `from app.api.routes import user` works.
Add new route modules here when you create them.
"""
from . import health, disease, crop_recommendation, user, feedback, devices, iot_webhook, integrations, llm_agent, voice  # noqa: F401



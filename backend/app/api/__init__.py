
# backend/app/api/__init__.py
"""
API package for AgroMind.

Expose a single APIRouter aggregator that main.py can include.
"""
from fastapi import APIRouter

api_router = APIRouter()

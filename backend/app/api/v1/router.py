"""
backend/app/api/v1/router.py

Aggregates all v1 endpoint routers under the /api/v1 prefix.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, inference

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(inference.router)

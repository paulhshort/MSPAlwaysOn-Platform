"""
API router aggregation.

This module imports and includes all API route modules.
"""

from fastapi import APIRouter

# Import endpoint modules
from .endpoints import auth, clients

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include authentication router
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include MSP-specific routers
api_router.include_router(clients.router, prefix="/clients", tags=["Clients"])

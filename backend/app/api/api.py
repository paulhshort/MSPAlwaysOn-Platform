"""
MSP-specific API router aggregation.

This module imports and includes all MSP-specific route modules.
"""

from fastapi import APIRouter

# Import route modules
# These will be implemented later based on your existing code
from .routes import alerts, agents, tickets, clients, webhooks

# Create main API router
api_router = APIRouter(prefix="/api/v1/msp")

# Include routers
api_router.include_router(alerts.router, prefix="/alerts", tags=["MSP Alerts"])
api_router.include_router(agents.router, prefix="/agents", tags=["MSP Agents"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["MSP Tickets"])
api_router.include_router(clients.router, prefix="/clients", tags=["MSP Clients"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["MSP Webhooks"])

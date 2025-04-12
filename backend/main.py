"""
MSPAlwaysOn - Main Application Entry Point

This module initializes the FastAPI application, integrating both MSP-specific
functionality and Keep.dev components.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import MSP-specific routers
from app.api.api import api_router as msp_api_router

# Import Keep.dev integration
from keep_integration import initialize_keep_integration
from keep_integration.api import keep_api_router

# Configure environment variables
# Load from .env file if available
from dotenv import load_dotenv
load_dotenv()

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Next.js dev server
    # Add production URLs as needed
]

# Initialize FastAPI app
app = FastAPI(
    title="MSPAlwaysOn",
    description="Unified AIOps and alert management platform for MSPs",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include MSP-specific API router
app.include_router(msp_api_router)

# Include Keep.dev API router
app.include_router(keep_api_router)

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint providing basic information about the API."""
    return {
        "message": "Welcome to MSPAlwaysOn API",
        "documentation": "/api/v1/docs",
        "version": "0.1.0"
    }

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize connections and resources on startup."""
    print("Starting MSPAlwaysOn API...")
    # Initialize Keep.dev integration
    initialize_keep_integration()
    # Initialize database connections, etc.

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    print("Shutting down MSPAlwaysOn API...")
    # Clean up resources

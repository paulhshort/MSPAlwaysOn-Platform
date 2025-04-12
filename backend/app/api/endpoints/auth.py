"""
Authentication API endpoints.
"""

import logging
from typing import Dict, Any
import httpx
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import Token, User, get_current_active_user
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    """
    Get an access token using Azure AD authentication.
    
    Args:
        form_data: OAuth2 password request form
        
    Returns:
        Access token
    """
    # Azure AD token endpoint
    token_url = f"https://login.microsoftonline.com/{settings.AZURE_AD_TENANT_ID}/oauth2/v2.0/token"
    
    # Request body
    data = {
        "client_id": settings.AZURE_AD_CLIENT_ID,
        "client_secret": settings.AZURE_AD_CLIENT_SECRET,
        "grant_type": "password",
        "username": form_data.username,
        "password": form_data.password,
        "scope": f"openid profile email {settings.AZURE_AD_CLIENT_ID}/.default"
    }
    
    try:
        # Make request to Azure AD
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            
            # Parse response
            token_data = response.json()
            
            # Return token
            return {
                "access_token": token_data["access_token"],
                "token_type": "bearer",
                "expires_in": token_data["expires_in"]
            }
    except httpx.HTTPStatusError as e:
        logger.error(f"Error authenticating with Azure AD: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication error",
        )

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Get the current user.
    
    Args:
        current_user: Current user
        
    Returns:
        User object
    """
    return current_user

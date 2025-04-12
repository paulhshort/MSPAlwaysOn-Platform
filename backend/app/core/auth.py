"""
Authentication module for MSPAlwaysOn.

This module provides authentication functionality using Azure AD.
"""

import os
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

# Azure AD configuration
AZURE_AD_TENANT_ID = os.environ.get("AZURE_AD_TENANT_ID", "")
AZURE_AD_CLIENT_ID = os.environ.get("AZURE_AD_CLIENT_ID", "")
AZURE_AD_CLIENT_SECRET = os.environ.get("AZURE_AD_CLIENT_SECRET", "")
AZURE_AD_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}"
AZURE_AD_JWKS_URI = f"{AZURE_AD_AUTHORITY}/discovery/v2.0/keys"

# JWT configuration
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class Token(BaseModel):
    """Token model."""
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    """Token data model."""
    sub: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    roles: List[str] = []
    exp: Optional[int] = None

class User(BaseModel):
    """User model."""
    id: str
    name: str
    email: str
    roles: List[str] = []
    is_active: bool = True

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the token.
    
    Args:
        token: JWT token
        
    Returns:
        User object
        
    Raises:
        HTTPException: If the token is invalid or the user is not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(
            token, 
            key=settings.JWT_PUBLIC_KEY, 
            algorithms=[ALGORITHM],
            audience=AZURE_AD_CLIENT_ID
        )
        
        # Extract user information
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        
        # Create token data
        token_data = TokenData(
            sub=sub,
            name=payload.get("name"),
            email=payload.get("email"),
            roles=payload.get("roles", []),
            exp=payload.get("exp")
        )
        
        # Check if token is expired
        if token_data.exp and datetime.utcnow() > datetime.fromtimestamp(token_data.exp):
            raise credentials_exception
        
        # Create user object
        user = User(
            id=token_data.sub,
            name=token_data.name or "",
            email=token_data.email or "",
            roles=token_data.roles
        )
        
        return user
    except JWTError:
        raise credentials_exception

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current user
        
    Returns:
        User object
        
    Raises:
        HTTPException: If the user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def has_role(required_roles: List[str]):
    """
    Check if the user has the required roles.
    
    Args:
        required_roles: List of required roles
        
    Returns:
        Dependency function
    """
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        for role in required_roles:
            if role in current_user.roles:
                return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return role_checker

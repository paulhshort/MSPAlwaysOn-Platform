"""
Client schemas.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ClientBase(BaseModel):
    """Base client schema."""
    name: str
    external_id: Optional[str] = None
    external_system: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    is_active: bool = True
    metadata: Optional[Dict[str, Any]] = None

class ClientCreate(ClientBase):
    """Client creation schema."""
    pass

class ClientUpdate(BaseModel):
    """Client update schema."""
    name: Optional[str] = None
    external_id: Optional[str] = None
    external_system: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

class ClientResponse(ClientBase):
    """Client response schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        """Pydantic config."""
        orm_mode = True

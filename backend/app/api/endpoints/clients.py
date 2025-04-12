"""
Client API endpoints.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.base_class import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.core.auth import User, get_current_active_user, has_role

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user)
) -> List[ClientResponse]:
    """
    Get all clients.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        name: Filter by name
        is_active: Filter by active status
        current_user: Current user
        
    Returns:
        List of clients
    """
    query = select(Client)
    
    # Apply filters
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if is_active is not None:
        query = query.filter(Client.is_active == is_active)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    clients = result.scalars().all()
    
    return clients

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ClientResponse:
    """
    Get a client by ID.
    
    Args:
        client_id: Client ID
        db: Database session
        current_user: Current user
        
    Returns:
        Client
    """
    result = await db.execute(select(Client).filter(Client.id == client_id))
    client = result.scalars().first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return client

@router.post("/", response_model=ClientResponse)
async def create_client(
    client: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(has_role(["admin"]))
) -> ClientResponse:
    """
    Create a new client.
    
    Args:
        client: Client data
        db: Database session
        current_user: Current user with admin role
        
    Returns:
        Created client
    """
    # Create client
    db_client = Client(**client.dict())
    
    # Add to database
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    
    return db_client

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(has_role(["admin"]))
) -> ClientResponse:
    """
    Update a client.
    
    Args:
        client_id: Client ID
        client: Client data
        db: Database session
        current_user: Current user with admin role
        
    Returns:
        Updated client
    """
    # Get client
    result = await db.execute(select(Client).filter(Client.id == client_id))
    db_client = result.scalars().first()
    
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Update client
    client_data = client.dict(exclude_unset=True)
    for key, value in client_data.items():
        setattr(db_client, key, value)
    
    # Save changes
    await db.commit()
    await db.refresh(db_client)
    
    return db_client

@router.delete("/{client_id}", response_model=ClientResponse)
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(has_role(["admin"]))
) -> ClientResponse:
    """
    Delete a client.
    
    Args:
        client_id: Client ID
        db: Database session
        current_user: Current user with admin role
        
    Returns:
        Deleted client
    """
    # Get client
    result = await db.execute(select(Client).filter(Client.id == client_id))
    db_client = result.scalars().first()
    
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Delete client
    await db.delete(db_client)
    await db.commit()
    
    return db_client

"""
Base class for SQLAlchemy models.
"""

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
import os

# Create a base class for all models
class CustomBase:
    """Custom base class for all models."""
    
    @declared_attr
    def __tablename__(cls):
        """Generate __tablename__ automatically."""
        return cls.__name__.lower()

Base = declarative_base(cls=CustomBase)

# Create async engine and session
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/mspalwayson")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Get a database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

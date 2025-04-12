"""
Asset model for MSPAlwaysOn.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base_class import Base

class AssetType(enum.Enum):
    """Enum for asset types."""
    WORKSTATION = "workstation"
    SERVER = "server"
    NETWORK = "network"
    MOBILE = "mobile"
    PRINTER = "printer"
    OTHER = "other"

class Asset(Base):
    """
    Asset model.
    
    This model represents a physical or virtual asset managed by the MSP.
    """
    
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    external_id = Column(String, index=True, unique=True, nullable=True)  # ID in external system
    external_system = Column(String, nullable=True)  # Name of external system (e.g., "rmm")
    
    # Asset information
    asset_type = Column(Enum(AssetType), nullable=False, default=AssetType.OTHER)
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    
    # Network information
    hostname = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    mac_address = Column(String, nullable=True)
    
    # Operating system information
    os_type = Column(String, nullable=True)
    os_version = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_monitored = Column(Boolean, default=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_seen = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    site = relationship("Site", back_populates="assets")
    
    def __repr__(self):
        return f"<Asset {self.name} (Site: {self.site_id})>"

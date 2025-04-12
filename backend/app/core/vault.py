"""
HashiCorp Vault integration for secure credential management.
"""

import os
import logging
import hvac
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class VaultClient:
    """
    Client for interacting with HashiCorp Vault.
    
    This class provides methods for securely storing and retrieving
    credentials and other sensitive information.
    """
    
    def __init__(self):
        """Initialize the Vault client."""
        self.client = None
        self.initialized = False
        self._init_client()
    
    def _init_client(self):
        """Initialize the Vault client connection."""
        try:
            vault_url = os.environ.get("VAULT_ADDR", "http://localhost:8200")
            vault_token = os.environ.get("VAULT_TOKEN", "mspalwayson-dev-token")
            
            self.client = hvac.Client(url=vault_url, token=vault_token)
            
            if not self.client.is_authenticated():
                logger.error("Failed to authenticate with Vault")
                return
            
            # Enable the KV secrets engine if not already enabled
            if "kv" not in self.client.sys.list_mounted_secrets_engines():
                self.client.sys.enable_secrets_engine(
                    backend_type="kv",
                    path="kv",
                    options={"version": "2"}
                )
            
            self.initialized = True
            logger.info("Vault client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Vault client: {e}")
            self.client = None
    
    def store_credentials(self, provider_id: str, credentials: Dict[str, Any]) -> bool:
        """
        Store provider credentials in Vault.
        
        Args:
            provider_id: Unique identifier for the provider
            credentials: Dictionary of credentials to store
            
        Returns:
            True if successful, False otherwise
        """
        if not self.initialized:
            logger.error("Vault client not initialized")
            return False
        
        try:
            path = f"kv/providers/{provider_id}"
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=credentials
            )
            logger.info(f"Stored credentials for provider {provider_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing credentials for provider {provider_id}: {e}")
            return False
    
    def get_credentials(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve provider credentials from Vault.
        
        Args:
            provider_id: Unique identifier for the provider
            
        Returns:
            Dictionary of credentials or None if not found
        """
        if not self.initialized:
            logger.error("Vault client not initialized")
            return None
        
        try:
            path = f"kv/providers/{provider_id}"
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response["data"]["data"]
        except Exception as e:
            logger.error(f"Error retrieving credentials for provider {provider_id}: {e}")
            return None
    
    def delete_credentials(self, provider_id: str) -> bool:
        """
        Delete provider credentials from Vault.
        
        Args:
            provider_id: Unique identifier for the provider
            
        Returns:
            True if successful, False otherwise
        """
        if not self.initialized:
            logger.error("Vault client not initialized")
            return False
        
        try:
            path = f"kv/providers/{provider_id}"
            self.client.secrets.kv.v2.delete_metadata_and_all_versions(path=path)
            logger.info(f"Deleted credentials for provider {provider_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting credentials for provider {provider_id}: {e}")
            return False

# Singleton instance
vault_client = VaultClient()

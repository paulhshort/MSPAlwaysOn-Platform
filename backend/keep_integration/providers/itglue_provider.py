"""
IT Glue Provider for Keep.dev

This module implements a Keep.dev provider for IT Glue,
allowing Keep to interact with IT Glue documentation and assets.
"""

from typing import Any, Dict, List, Optional
import logging
import httpx
from datetime import datetime

from keep.providers.base.base_provider import BaseProvider
from keep.providers.models.provider_config import ProviderConfig

logger = logging.getLogger(__name__)

class ITGlueProvider(BaseProvider):
    """
    IT Glue provider for Keep.dev.

    This provider allows Keep to:
    1. Query organizations, configurations, and documents from IT Glue
    2. Enrich alerts with IT Glue data
    3. Create and update IT Glue documents
    """

    PROVIDER_DISPLAY_NAME = "IT Glue"
    PROVIDER_CATEGORY = ["Documentation", "ITAM"]
    PROVIDER_TAGS = ["msp", "documentation", "itam"]
    PROVIDER_DESCRIPTION = "IT Glue is a documentation platform for MSPs."
    FINGERPRINT_FIELDS = ["id", "name"]

    def __init__(self, provider_id, config):
        super().__init__(provider_id, config)
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize the IT Glue client."""
        try:
            auth_config = self.config.authentication
            self.api_key = auth_config.get("api_key")
            self.base_url = auth_config.get("base_url", "https://api.itglue.com")

            # Validate required configuration
            if not self.api_key:
                logger.error("Missing required IT Glue authentication configuration")
                return

            # Initialize HTTP client with authentication headers
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "x-api-key": self.api_key,
                    "Content-Type": "application/vnd.api+json"
                },
                timeout=30.0
            )
            logger.info(f"IT Glue client initialized")
        except Exception as e:
            logger.error(f"Error initializing IT Glue client: {e}")
            self.client = None

    async def query(self, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query IT Glue resources.

        Args:
            query_params: Parameters for the query
                - resource_type: Type of resource (organizations, configurations, documents, etc.)
                - filters: Dictionary of filters
                - page: Page number (default: 1)
                - page_size: Page size (default: 50)
                - organization_id: Optional organization ID for scoped resources
                - client_id: Optional MSPAlwaysOn client ID to map to IT Glue organization

        Returns:
            List of resources matching the query
        """
        if not self.client:
            logger.error("IT Glue client not initialized")
            return []

        try:
            # Extract query parameters
            resource_type = query_params.get("resource_type", "organizations")
            filters = query_params.get("filters", {})
            page = query_params.get("page", 1)
            page_size = query_params.get("page_size", 50)
            organization_id = query_params.get("organization_id")
            client_id = query_params.get("client_id")

            # If client_id is provided but organization_id is not, map client to organization
            if client_id and not organization_id:
                org_mapping = await self._get_organization_by_client_id(client_id)
                if org_mapping and "organization_id" in org_mapping:
                    organization_id = org_mapping["organization_id"]

            # Build query parameters
            params = {
                "page[number]": page,
                "page[size]": page_size
            }

            # Add filters if provided
            if filters:
                for key, value in filters.items():
                    params[f"filter[{key}]"] = value

            # Determine endpoint based on resource type
            if resource_type == "organizations":
                endpoint = "/organizations"
            elif resource_type == "configurations":
                if organization_id:
                    endpoint = f"/organizations/{organization_id}/configurations"
                else:
                    endpoint = "/configurations"
            elif resource_type == "passwords":
                if organization_id:
                    endpoint = f"/organizations/{organization_id}/passwords"
                else:
                    endpoint = "/passwords"
            elif resource_type == "documents":
                if organization_id:
                    endpoint = f"/organizations/{organization_id}/documents"
                else:
                    endpoint = "/documents"
            elif resource_type == "contacts":
                if organization_id:
                    endpoint = f"/organizations/{organization_id}/contacts"
                else:
                    endpoint = "/contacts"
            else:
                logger.error(f"Unsupported resource type: {resource_type}")
                return []

            # Make API request
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()

            # Parse response
            data = response.json().get("data", [])

            # Transform data to a more usable format
            return [self._transform_resource(item, resource_type) for item in data]
        except Exception as e:
            logger.error(f"Error querying IT Glue: {e}")
            return []

    async def notify(self, notification_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update IT Glue resources.

        Args:
            notification_params: Parameters for the notification
                - action: Action to perform (create, update)
                - resource_type: Type of resource (organizations, configurations, documents, etc.)
                - resource_id: ID of the resource (for update)
                - organization_id: Optional organization ID for scoped resources
                - data: Resource data

        Returns:
            Created or updated resource
        """
        if not self.client:
            logger.error("IT Glue client not initialized")
            return {"success": False, "message": "Client not initialized"}

        try:
            # Extract parameters
            action = notification_params.get("action")
            resource_type = notification_params.get("resource_type")
            resource_id = notification_params.get("resource_id")
            organization_id = notification_params.get("organization_id")
            data = notification_params.get("data", {})

            if not action or not resource_type or not data:
                return {"success": False, "message": "Action, resource_type, and data are required"}

            # Format data for IT Glue API
            formatted_data = {
                "data": {
                    "type": resource_type,
                    "attributes": data
                }
            }

            # Perform action based on type
            if action == "create":
                return await self._create_resource(resource_type, organization_id, formatted_data)
            elif action == "update" and resource_id:
                return await self._update_resource(resource_type, resource_id, organization_id, formatted_data)
            else:
                return {"success": False, "message": f"Unsupported action: {action} or missing resource_id for update"}
        except Exception as e:
            logger.error(f"Error in IT Glue notify operation: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    async def _create_resource(self, resource_type: str, organization_id: Optional[str], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a resource in IT Glue.

        Args:
            resource_type: Type of resource
            organization_id: Optional organization ID for scoped resources
            data: Resource data

        Returns:
            Created resource
        """
        # Determine endpoint based on resource type
        if resource_type == "organizations":
            endpoint = "/organizations"
        elif resource_type == "configurations":
            if organization_id:
                endpoint = f"/organizations/{organization_id}/configurations"
            else:
                return {"success": False, "message": "organization_id is required for configurations"}
        elif resource_type == "passwords":
            if organization_id:
                endpoint = f"/organizations/{organization_id}/passwords"
            else:
                return {"success": False, "message": "organization_id is required for passwords"}
        elif resource_type == "documents":
            if organization_id:
                endpoint = f"/organizations/{organization_id}/documents"
            else:
                return {"success": False, "message": "organization_id is required for documents"}
        elif resource_type == "contacts":
            if organization_id:
                endpoint = f"/organizations/{organization_id}/contacts"
            else:
                return {"success": False, "message": "organization_id is required for contacts"}
        else:
            return {"success": False, "message": f"Unsupported resource type: {resource_type}"}

        # Make API request
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()

        # Parse response
        result = response.json().get("data", {})

        return {
            "success": True,
            "message": f"{resource_type.capitalize()} created successfully",
            "resource": self._transform_resource(result, resource_type),
            "resource_id": result.get("id")
        }

    async def _update_resource(self, resource_type: str, resource_id: str, organization_id: Optional[str], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a resource in IT Glue.

        Args:
            resource_type: Type of resource
            resource_id: ID of the resource
            organization_id: Optional organization ID for scoped resources
            data: Resource data

        Returns:
            Updated resource
        """
        # Determine endpoint based on resource type
        if resource_type == "organizations":
            endpoint = f"/organizations/{resource_id}"
        elif resource_type == "configurations":
            endpoint = f"/configurations/{resource_id}"
        elif resource_type == "passwords":
            endpoint = f"/passwords/{resource_id}"
        elif resource_type == "documents":
            endpoint = f"/documents/{resource_id}"
        elif resource_type == "contacts":
            endpoint = f"/contacts/{resource_id}"
        else:
            return {"success": False, "message": f"Unsupported resource type: {resource_type}"}

        # Make API request
        response = await self.client.patch(endpoint, json=data)
        response.raise_for_status()

        # Parse response
        result = response.json().get("data", {})

        return {
            "success": True,
            "message": f"{resource_type.capitalize()} updated successfully",
            "resource": self._transform_resource(result, resource_type),
            "resource_id": result.get("id")
        }

    async def _get_organization_by_client_id(self, client_id: str) -> Dict[str, Any]:
        """
        Get IT Glue organization ID by MSPAlwaysOn client ID.

        This method maps an MSPAlwaysOn client ID to an IT Glue organization ID.

        Args:
            client_id: MSPAlwaysOn client ID

        Returns:
            Dictionary with organization_id and other mapping information
        """
        try:
            # Query the database for client information
            from sqlalchemy.ext.asyncio import AsyncSession
            from sqlalchemy.future import select
            from app.db.base_class import get_db
            from app.models.client import Client

            # Get database session
            db_session = None
            async for session in get_db():
                db_session = session
                break

            if not db_session:
                logger.error("Failed to get database session")
                return {}

            # Query client by ID
            result = await db_session.execute(select(Client).where(Client.id == int(client_id)))
            client = result.scalars().first()

            if not client:
                logger.error(f"Client with ID {client_id} not found")
                return {}

            # Get client name and external IT Glue organization ID if available
            client_name = client.name
            external_id = client.external_id if client.external_system == "itglue" else None

            # If we have a direct mapping via external_id, use it
            if external_id:
                return {
                    "client_id": client_id,
                    "client_name": client_name,
                    "organization_id": external_id,
                    "direct_mapping": True
                }

            # Search for organizations with matching name
            params = {
                "filter[name]": client_name,
                "page[size]": 1
            }

            response = await self.client.get("/organizations", params=params)
            response.raise_for_status()

            data = response.json().get("data", [])

            if not data:
                logger.warning(f"No IT Glue organization found for client ID {client_id}")
                return {}

            # Get the first matching organization
            organization = data[0]
            organization_id = organization.get("id")

            if not organization_id:
                logger.warning(f"No valid organization ID found for client ID {client_id}")
                return {}

            # Return the mapping
            return {
                "client_id": client_id,
                "client_name": client_name,
                "organization_id": organization_id,
                "organization_name": organization.get("attributes", {}).get("name")
            }
        except Exception as e:
            logger.error(f"Error mapping client to IT Glue organization: {e}")
            return {}

    def _transform_resource(self, resource: Dict[str, Any], resource_type: str) -> Dict[str, Any]:
        """
        Transform an IT Glue resource to a more usable format.

        Args:
            resource: IT Glue resource
            resource_type: Type of resource

        Returns:
            Transformed resource
        """
        # Extract ID and attributes
        resource_id = resource.get("id")
        attributes = resource.get("attributes", {})

        # Create base transformed resource
        transformed = {
            "id": resource_id,
            "type": resource_type
        }

        # Add attributes
        transformed.update(attributes)

        # Add relationships if present
        if "relationships" in resource:
            relationships = resource.get("relationships", {})
            transformed["relationships"] = {}

            for rel_name, rel_data in relationships.items():
                if "data" in rel_data:
                    rel_data = rel_data.get("data")
                    if isinstance(rel_data, list):
                        transformed["relationships"][rel_name] = [{"id": item.get("id"), "type": item.get("type")} for item in rel_data]
                    elif rel_data:
                        transformed["relationships"][rel_name] = {"id": rel_data.get("id"), "type": rel_data.get("type")}

        return transformed

"""
SentinelOne Provider for Keep.dev

This module implements a Keep.dev provider for SentinelOne,
allowing Keep to interact with SentinelOne threats and endpoints.
"""

from typing import Any, Dict, List, Optional
import logging
import httpx
from datetime import datetime, timedelta

from keep.providers.base.base_provider import BaseProvider
from keep.providers.models.provider_config import ProviderConfig

logger = logging.getLogger(__name__)

class SentinelOneProvider(BaseProvider):
    """
    SentinelOne provider for Keep.dev.

    This provider allows Keep to:
    1. Query threats and events from SentinelOne
    2. Perform actions on endpoints (isolate, reconnect, etc.)
    3. Sync alerts between Keep and SentinelOne
    """

    PROVIDER_DISPLAY_NAME = "SentinelOne"
    PROVIDER_CATEGORY = ["Security", "EDR"]
    PROVIDER_TAGS = ["msp", "security", "edr", "xdr"]
    PROVIDER_DESCRIPTION = "SentinelOne is an endpoint protection platform that uses AI to prevent, detect, and respond to threats."
    FINGERPRINT_FIELDS = ["id", "threatInfo.threatName"]

    def __init__(self, provider_id, config):
        super().__init__(provider_id, config)
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize the SentinelOne client."""
        try:
            auth_config = self.config.authentication
            self.api_token = auth_config.get("api_token")
            self.base_url = auth_config.get("base_url", "https://usea1-partners.sentinelone.net/api")
            self.account_id = auth_config.get("account_id")

            # Validate required configuration
            if not all([self.api_token, self.base_url]):
                logger.error("Missing required SentinelOne authentication configuration")
                return

            # Initialize HTTP client with authentication headers
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Authorization": f"ApiToken {self.api_token}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            logger.info(f"SentinelOne client initialized")
        except Exception as e:
            logger.error(f"Error initializing SentinelOne client: {e}")
            self.client = None

    async def query(self, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query threats from SentinelOne.

        Args:
            query_params: Parameters for the query
                - query_type: Type of query (threats, agents, activities, groups, sites)
                - filters: Dictionary of filters
                - limit: Maximum number of results (default: 25)
                - cursor: Pagination cursor
                - client_id: Optional client ID to filter by site

        Returns:
            List of threats matching the query
        """
        if not self.client:
            logger.error("SentinelOne client not initialized")
            return []

        try:
            # Extract query parameters
            query_type = query_params.get("query_type", "threats")
            filters = query_params.get("filters", {})
            limit = query_params.get("limit", 25)
            cursor = query_params.get("cursor")
            client_id = query_params.get("client_id")

            # If client_id is provided, get the site IDs for this client
            site_ids = []
            if client_id:
                site_mapping = await self._get_client_site_mapping(client_id)
                if site_mapping and "site_ids" in site_mapping:
                    site_ids = site_mapping["site_ids"]

            # Build query parameters
            params = {
                "limit": limit,
                "accountIds": self.account_id
            }

            # Add site IDs filter if available
            if site_ids:
                params["siteIds"] = ",".join(site_ids)

            # Add cursor if provided
            if cursor:
                params["cursor"] = cursor

            # Add filters if provided
            if filters:
                for key, value in filters.items():
                    params[key] = value

            # Determine endpoint based on query type
            if query_type == "threats":
                endpoint = "/v2/threats"
            elif query_type == "agents":
                endpoint = "/v2/agents"
            elif query_type == "activities":
                endpoint = "/v2/activities"
            elif query_type == "groups":
                endpoint = "/v2/groups"
            elif query_type == "sites":
                endpoint = "/v2/sites"
            else:
                logger.error(f"Unsupported query type: {query_type}")
                return []

            # Make API request
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()

            # Parse response
            data = response.json()

            # Extract items based on query type
            if query_type == "threats":
                items = data.get("data", {}).get("threats", [])
                return [self._transform_threat_to_alert(threat) for threat in items]
            elif query_type == "agents":
                items = data.get("data", {}).get("agents", [])
                return items
            elif query_type == "activities":
                items = data.get("data", {}).get("activities", [])
                return items
            elif query_type == "groups":
                items = data.get("data", {}).get("groups", [])
                return items
            elif query_type == "sites":
                items = data.get("data", {}).get("sites", [])
                return items

            return []
        except Exception as e:
            logger.error(f"Error querying SentinelOne: {e}")
            return []

    async def notify(self, notification_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on SentinelOne endpoints or threats.

        Args:
            notification_params: Parameters for the action
                - action: Action to perform (isolate, reconnect, mitigate, etc.)
                - agent_ids: List of agent IDs (for agent actions)
                - threat_ids: List of threat IDs (for threat actions)

        Returns:
            Result of the action
        """
        if not self.client:
            logger.error("SentinelOne client not initialized")
            return {"success": False, "message": "Client not initialized"}

        try:
            # Extract parameters
            action = notification_params.get("action")
            agent_ids = notification_params.get("agent_ids", [])
            threat_ids = notification_params.get("threat_ids", [])

            if not action:
                return {"success": False, "message": "Action is required"}

            # Perform action based on type
            if action == "isolate" and agent_ids:
                return await self._isolate_agents(agent_ids)
            elif action == "reconnect" and agent_ids:
                return await self._reconnect_agents(agent_ids)
            elif action == "mitigate" and threat_ids:
                return await self._mitigate_threats(threat_ids)
            elif action == "get_endpoint_by_threat_id" and threat_ids:
                return await self._get_endpoint_by_threat_id(threat_ids[0])
            elif action == "get_threat_details" and threat_ids:
                return await self._get_threat_details(threat_ids[0])
            else:
                return {"success": False, "message": f"Unsupported action: {action}"}
        except Exception as e:
            logger.error(f"Error in SentinelOne notify operation: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    async def _isolate_agents(self, agent_ids: List[str]) -> Dict[str, Any]:
        """
        Isolate agents from the network.

        Args:
            agent_ids: List of agent IDs to isolate

        Returns:
            Result of the isolation
        """
        endpoint = "/v2/agents/actions/disconnect"
        data = {
            "filter": {
                "ids": agent_ids
            }
        }

        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()

        result = response.json()
        return {
            "success": result.get("data", {}).get("affected", 0) > 0,
            "message": "Agents isolated successfully" if result.get("data", {}).get("affected", 0) > 0 else "No agents were isolated",
            "affected": result.get("data", {}).get("affected", 0),
            "result": result
        }

    async def _reconnect_agents(self, agent_ids: List[str]) -> Dict[str, Any]:
        """
        Reconnect isolated agents to the network.

        Args:
            agent_ids: List of agent IDs to reconnect

        Returns:
            Result of the reconnection
        """
        endpoint = "/v2/agents/actions/connect"
        data = {
            "filter": {
                "ids": agent_ids
            }
        }

        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()

        result = response.json()
        return {
            "success": result.get("data", {}).get("affected", 0) > 0,
            "message": "Agents reconnected successfully" if result.get("data", {}).get("affected", 0) > 0 else "No agents were reconnected",
            "affected": result.get("data", {}).get("affected", 0),
            "result": result
        }

    async def _mitigate_threats(self, threat_ids: List[str]) -> Dict[str, Any]:
        """
        Mitigate threats.

        Args:
            threat_ids: List of threat IDs to mitigate

        Returns:
            Result of the mitigation
        """
        endpoint = "/v2/threats/mitigate"
        data = {
            "filter": {
                "ids": threat_ids
            },
            "action": "mitigate"
        }

        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()

        result = response.json()
        return {
            "success": result.get("data", {}).get("affected", 0) > 0,
            "message": "Threats mitigated successfully" if result.get("data", {}).get("affected", 0) > 0 else "No threats were mitigated",
            "affected": result.get("data", {}).get("affected", 0),
            "result": result
        }

    async def _get_threat_details(self, threat_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a threat.

        Args:
            threat_id: ID of the threat

        Returns:
            Detailed threat information
        """
        endpoint = f"/v2/threats/{threat_id}"

        try:
            response = await self.client.get(endpoint)
            response.raise_for_status()

            threat_data = response.json().get("data", {})

            # Get additional threat information
            threat_info = threat_data.get("threatInfo", {})
            indicators = []

            # Get indicators of compromise if available
            if "indicators" in threat_data:
                indicators = threat_data.get("indicators", [])

            # Get timeline events if available
            timeline = []
            timeline_endpoint = f"/v2/threats/{threat_id}/timeline"
            try:
                timeline_response = await self.client.get(timeline_endpoint)
                if timeline_response.status_code == 200:
                    timeline_data = timeline_response.json()
                    timeline = timeline_data.get("data", {}).get("timeline", [])
            except Exception as e:
                logger.warning(f"Error getting threat timeline: {e}")

            return {
                "success": True,
                "message": "Threat details retrieved successfully",
                "threat_id": threat_id,
                "name": threat_info.get("threatName"),
                "classification": threat_info.get("classification"),
                "confidence_level": threat_info.get("confidenceLevel"),
                "severity": threat_info.get("severity"),
                "status": "Resolved" if threat_data.get("resolved") else "Active",
                "mitigated": threat_data.get("mitigationStatus") == "mitigated",
                "agent_details": {
                    "id": threat_data.get("agentId"),
                    "computer_name": threat_data.get("agentComputerName"),
                    "os": threat_data.get("agentOsType")
                },
                "site": {
                    "id": threat_data.get("siteId"),
                    "name": threat_data.get("siteName")
                },
                "indicators": indicators,
                "timeline": timeline,
                "created_at": threat_data.get("createdAt"),
                "updated_at": threat_data.get("updatedAt"),
                "raw_data": threat_data
            }
        except Exception as e:
            logger.error(f"Error getting threat details: {e}")
            return {
                "success": False,
                "message": f"Error getting threat details: {str(e)}"
            }

    async def _get_endpoint_by_threat_id(self, threat_id: str) -> Dict[str, Any]:
        """
        Get endpoint details by threat ID.

        Args:
            threat_id: ID of the threat

        Returns:
            Endpoint details
        """
        # First, get the threat details
        endpoint = f"/v2/threats/{threat_id}"

        response = await self.client.get(endpoint)
        response.raise_for_status()

        threat_data = response.json().get("data", {})
        agent_id = threat_data.get("agentId")

        if not agent_id:
            return {
                "success": False,
                "message": "Agent ID not found for threat"
            }

        # Now, get the agent details
        endpoint = f"/v2/agents/{agent_id}"

        response = await self.client.get(endpoint)
        response.raise_for_status()

        agent_data = response.json().get("data", {})

        return {
            "success": True,
            "message": "Endpoint details retrieved successfully",
            "endpoint_id": agent_id,
            "hostname": agent_data.get("computerName"),
            "ip_address": agent_data.get("lastIpToMgmt"),
            "mac_address": agent_data.get("networkInterfaces", [{}])[0].get("physical") if agent_data.get("networkInterfaces") else None,
            "os": agent_data.get("osName"),
            "version": agent_data.get("agentVersion"),
            "last_logged_in_user": agent_data.get("lastLoggedInUserName"),
            "is_isolated": agent_data.get("isActive") and agent_data.get("networkStatus") == "disconnected",
            "site_name": agent_data.get("siteName"),
            "group_name": agent_data.get("groupName"),
            "raw_data": agent_data
        }

    async def _get_client_site_mapping(self, client_id: str) -> Dict[str, Any]:
        """
        Get the mapping between a client ID and SentinelOne site IDs.

        This method queries the database to find the mapping between
        MSPAlwaysOn client IDs and SentinelOne site IDs.

        Args:
            client_id: MSPAlwaysOn client ID

        Returns:
            Dictionary with site_ids list and other mapping information
        """
        try:
            # Query sites endpoint to get all sites
            sites_response = await self.client.get("/v2/sites", params={"accountIds": self.account_id})
            sites_response.raise_for_status()

            sites_data = sites_response.json()
            sites = sites_data.get("data", {}).get("sites", [])

            # For now, we'll use a simple mapping based on site name
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

            # Get client name and metadata containing SentinelOne site IDs if available
            client_name = client.name
            metadata = client.metadata or {}
            sentinelone_sites = metadata.get("sentinelone_sites", [])

            # If we have direct site mappings in metadata, use them
            if sentinelone_sites:
                return {
                    "client_id": client_id,
                    "client_name": client_name,
                    "site_ids": [site.get("id") for site in sentinelone_sites if "id" in site],
                    "site_names": [site.get("name") for site in sentinelone_sites if "name" in site],
                    "direct_mapping": True
                }

            # Find sites that match the client name
            matching_sites = []
            for site in sites:
                # In a real implementation, you would have a more robust mapping
                if client_name.lower() in site.get("name", "").lower():
                    matching_sites.append(site)

            if not matching_sites:
                logger.warning(f"No SentinelOne sites found for client ID {client_id}")
                return {}

            # Return the mapping
            return {
                "client_id": client_id,
                "client_name": client_name,
                "site_ids": [site.get("id") for site in matching_sites],
                "site_names": [site.get("name") for site in matching_sites]
            }
        except Exception as e:
            logger.error(f"Error getting client-site mapping: {e}")
            return {}

    def _transform_threat_to_alert(self, threat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a SentinelOne threat to a Keep alert format.

        Args:
            threat: SentinelOne threat

        Returns:
            Keep alert
        """
        # Map threat severity to alert severity
        severity_map = {
            "Critical": "critical",
            "High": "warning",
            "Medium": "warning",
            "Low": "info",
            "Suspicious": "info"
        }

        # Get threat info
        threat_info = threat.get("threatInfo", {})

        # Map to Keep alert
        return {
            "id": str(threat.get("id")),
            "name": threat_info.get("threatName", "Unknown Threat"),
            "description": threat_info.get("threatDetails", ""),
            "source": "sentinelone",
            "severity": severity_map.get(threat_info.get("severity", ""), "info"),
            "status": "firing" if threat.get("resolved") is False else "resolved",
            "lastReceived": threat.get("createdAt", datetime.now().isoformat()),
            "fingerprint": f"sentinelone-{threat.get('id')}",
            "labels": {
                "site_name": threat.get("siteName", "Unknown"),
                "account_name": threat.get("accountName", "Unknown"),
                "computer_name": threat.get("agentComputerName", "Unknown"),
                "classification": threat_info.get("classification", "Unknown"),
                "confidence_level": threat_info.get("confidenceLevel", "Unknown"),
                "threat_name": threat_info.get("threatName", "Unknown")
            },
            "annotations": {
                "threat_id": str(threat.get("id")),
                "agent_id": str(threat.get("agentId")),
                "site_id": str(threat.get("siteId")),
                "account_id": str(threat.get("accountId")),
                "mitigated": str(threat.get("mitigationStatus") == "mitigated").lower(),
                "resolved": str(threat.get("resolved")).lower()
            },
            "raw_data": threat
        }

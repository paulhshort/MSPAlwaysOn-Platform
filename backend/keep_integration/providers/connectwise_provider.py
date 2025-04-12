"""
ConnectWise Manage Provider for Keep.dev

This module implements a Keep.dev provider for ConnectWise Manage,
allowing Keep to interact with ConnectWise tickets and alerts.
"""

from typing import Any, Dict, List, Optional, Union
import logging
import httpx
from datetime import datetime

from keep.providers.base.base_provider import BaseProvider
from keep.providers.models.provider_config import ProviderConfig

logger = logging.getLogger(__name__)

class ConnectWiseManageProviderAuthConfig:
    """Authentication configuration for ConnectWise Manage provider."""

    company_id: str
    public_key: str
    private_key: str
    client_id: str
    base_url: str

class ConnectWiseManageProvider(BaseProvider):
    """
    ConnectWise Manage provider for Keep.dev.

    This provider allows Keep to:
    1. Query tickets from ConnectWise Manage
    2. Create and update tickets in ConnectWise Manage
    3. Sync alerts between Keep and ConnectWise
    """

    PROVIDER_DISPLAY_NAME = "ConnectWise Manage"
    PROVIDER_CATEGORY = ["Ticketing", "PSA"]
    PROVIDER_TAGS = ["msp", "ticketing", "psa"]
    PROVIDER_DESCRIPTION = "ConnectWise Manage is a business management platform for MSPs."
    FINGERPRINT_FIELDS = ["id", "summary"]

    def __init__(self, provider_id, config):
        super().__init__(provider_id, config)
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize the ConnectWise client."""
        try:
            auth_config = self.config.authentication
            self.company_id = auth_config.get("company_id")
            self.public_key = auth_config.get("public_key")
            self.private_key = auth_config.get("private_key")
            self.client_id = auth_config.get("client_id")
            self.base_url = auth_config.get("base_url")

            # Validate required configuration
            if not all([self.company_id, self.public_key, self.private_key, self.client_id, self.base_url]):
                logger.error("Missing required ConnectWise Manage authentication configuration")
                return

            # Initialize HTTP client with authentication headers
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Basic {self._get_auth_header()}",
                    "ClientID": self.client_id,
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            logger.info(f"ConnectWise Manage client initialized for company {self.company_id}")
        except Exception as e:
            logger.error(f"Error initializing ConnectWise Manage client: {e}")
            self.client = None

    def _get_auth_header(self) -> str:
        """
        Generate the Basic Auth header for ConnectWise Manage API.

        Returns:
            Base64 encoded authorization string
        """
        import base64
        auth_string = f"{self.company_id}+{self.public_key}:{self.private_key}"
        return base64.b64encode(auth_string.encode()).decode()

    async def query(self, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query tickets from ConnectWise Manage.

        Args:
            query_params: Parameters for the query
                - conditions: List of condition dictionaries
                - page: Page number (default: 1)
                - page_size: Page size (default: 25)

        Returns:
            List of tickets matching the query
        """
        if not self.client:
            logger.error("ConnectWise Manage client not initialized")
            return []

        try:
            # Extract query parameters
            conditions = query_params.get("conditions", [])
            page = query_params.get("page", 1)
            page_size = query_params.get("page_size", 25)

            # Build query parameters
            params = {
                "page": page,
                "pageSize": page_size
            }

            # Add conditions if provided
            if conditions:
                condition_strings = []
                for condition in conditions:
                    field = condition.get("field")
                    operator = condition.get("operator", "equals")
                    value = condition.get("value")

                    if field and value is not None:
                        # Map operator to ConnectWise format
                        cw_operator = self._map_operator(operator)
                        condition_strings.append(f"{field} {cw_operator} {self._format_value(value)}")

                if condition_strings:
                    params["conditions"] = " AND ".join(condition_strings)

            # Make API request
            response = await self.client.get("/service/tickets", params=params)
            response.raise_for_status()

            # Parse response
            tickets = response.json()

            # Transform tickets to Keep format
            return [self._transform_ticket_to_alert(ticket) for ticket in tickets]
        except Exception as e:
            logger.error(f"Error querying ConnectWise Manage tickets: {e}")
            return []

    async def notify(self, notification_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update a ticket in ConnectWise Manage.

        Args:
            notification_params: Parameters for the notification
                - ticket_id: ID of the ticket to update (if updating)
                - summary: Ticket summary
                - description: Ticket description
                - company_id: Company ID
                - board_id: Board ID
                - status_id: Status ID
                - priority_id: Priority ID
                - etc.

        Returns:
            Created or updated ticket
        """
        if not self.client:
            logger.error("ConnectWise Manage client not initialized")
            return {"success": False, "message": "Client not initialized"}

        try:
            # Check if we're creating or updating
            ticket_id = notification_params.get("ticket_id")

            if ticket_id:
                # Update existing ticket
                return await self._update_ticket(ticket_id, notification_params)
            else:
                # Create new ticket
                return await self._create_ticket(notification_params)
        except Exception as e:
            logger.error(f"Error in ConnectWise Manage notify operation: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    async def _create_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new ticket in ConnectWise Manage.

        Args:
            params: Ticket parameters

        Returns:
            Created ticket
        """
        # Build ticket data
        ticket_data = {
            "summary": params.get("summary"),
            "initialDescription": params.get("description"),
            "board": {"id": params.get("board_id")},
            "company": {"id": params.get("company_id")},
            "status": {"id": params.get("status_id")} if params.get("status_id") else None,
            "priority": {"id": params.get("priority_id")} if params.get("priority_id") else None,
            "impact": {"id": params.get("impact_id")} if params.get("impact_id") else None,
            "contact": {"id": params.get("contact_id")} if params.get("contact_id") else None,
            "owner": {"id": params.get("owner_id")} if params.get("owner_id") else None,
            "type": {"id": params.get("type_id")} if params.get("type_id") else None,
            "subType": {"id": params.get("subtype_id")} if params.get("subtype_id") else None,
            "item": {"id": params.get("item_id")} if params.get("item_id") else None,
        }

        # Remove None values
        ticket_data = {k: v for k, v in ticket_data.items() if v is not None}

        # Make API request
        response = await self.client.post("/service/tickets", json=ticket_data)
        response.raise_for_status()

        # Parse response
        created_ticket = response.json()

        return {
            "success": True,
            "message": "Ticket created successfully",
            "ticket": created_ticket,
            "ticket_id": created_ticket.get("id")
        }

    async def _update_ticket(self, ticket_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing ticket in ConnectWise Manage.

        Args:
            ticket_id: ID of the ticket to update
            params: Ticket parameters to update

        Returns:
            Updated ticket
        """
        # Build ticket data
        ticket_data = {}

        # Map parameters to ticket fields
        field_mappings = {
            "summary": "summary",
            "status_id": ("status", "id"),
            "priority_id": ("priority", "id"),
            "impact_id": ("impact", "id"),
            "board_id": ("board", "id"),
            "company_id": ("company", "id"),
            "contact_id": ("contact", "id"),
            "owner_id": ("owner", "id"),
            "type_id": ("type", "id"),
            "subtype_id": ("subType", "id"),
            "item_id": ("item", "id"),
        }

        for param_key, field_key in field_mappings.items():
            if param_key in params and params[param_key] is not None:
                if isinstance(field_key, tuple):
                    # Handle nested fields
                    parent_key, child_key = field_key
                    if parent_key not in ticket_data:
                        ticket_data[parent_key] = {}
                    ticket_data[parent_key][child_key] = params[param_key]
                else:
                    # Handle direct fields
                    ticket_data[field_key] = params[param_key]

        # Make API request
        response = await self.client.patch(f"/service/tickets/{ticket_id}", json=ticket_data)
        response.raise_for_status()

        # Parse response
        updated_ticket = response.json()

        return {
            "success": True,
            "message": "Ticket updated successfully",
            "ticket": updated_ticket,
            "ticket_id": updated_ticket.get("id")
        }

    async def _add_ticket_note(self, ticket_id: int, note_text: str, internal: bool = False) -> Dict[str, Any]:
        """
        Add a note to a ticket in ConnectWise Manage.

        Args:
            ticket_id: ID of the ticket
            note_text: Text of the note
            internal: Whether the note is internal

        Returns:
            Created note
        """
        # Build note data
        note_data = {
            "text": note_text,
            "internalAnalysisFlag": internal,
            "detailDescriptionFlag": False,
            "resolutionFlag": False,
            "externalFlag": not internal
        }

        # Make API request
        response = await self.client.post(f"/service/tickets/{ticket_id}/notes", json=note_data)
        response.raise_for_status()

        # Parse response
        created_note = response.json()

        return {
            "success": True,
            "message": "Note added successfully",
            "note": created_note
        }

    def _transform_ticket_to_alert(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a ConnectWise Manage ticket to a Keep alert format.

        Args:
            ticket: ConnectWise Manage ticket

        Returns:
            Keep alert
        """
        # Map ticket status to alert severity
        severity_map = {
            "New": "critical",
            "In Progress": "warning",
            "Waiting Customer": "info",
            "Resolved": "info",
            "Closed": "info"
        }

        # Get status name
        status_name = ticket.get("status", {}).get("name", "Unknown")

        # Map to Keep alert
        return {
            "id": str(ticket.get("id")),
            "name": ticket.get("summary", "No summary"),
            "description": ticket.get("initialDescription", ""),
            "source": "connectwise-manage",
            "severity": severity_map.get(status_name, "info"),
            "status": "firing" if status_name not in ["Resolved", "Closed"] else "resolved",
            "lastReceived": ticket.get("_info", {}).get("lastUpdated", datetime.now().isoformat()),
            "fingerprint": f"connectwise-manage-{ticket.get('id')}",
            "labels": {
                "company": ticket.get("company", {}).get("name", "Unknown"),
                "board": ticket.get("board", {}).get("name", "Unknown"),
                "status": status_name,
                "priority": ticket.get("priority", {}).get("name", "Unknown"),
                "owner": ticket.get("owner", {}).get("identifier", "Unassigned")
            },
            "annotations": {
                "ticket_id": str(ticket.get("id")),
                "company_id": str(ticket.get("company", {}).get("id", "")),
                "board_id": str(ticket.get("board", {}).get("id", "")),
                "status_id": str(ticket.get("status", {}).get("id", "")),
                "priority_id": str(ticket.get("priority", {}).get("id", "")),
                "owner_id": str(ticket.get("owner", {}).get("id", ""))
            },
            "raw_data": ticket
        }

    def _map_operator(self, operator: str) -> str:
        """
        Map a standard operator to ConnectWise Manage format.

        Args:
            operator: Standard operator

        Returns:
            ConnectWise Manage operator
        """
        operator_map = {
            "equals": "=",
            "not_equals": "!=",
            "greater_than": ">",
            "less_than": "<",
            "greater_than_or_equals": ">=",
            "less_than_or_equals": "<=",
            "contains": "contains",
            "like": "like",
            "in": "in",
            "not_in": "not in",
            "is_null": "is null",
            "is_not_null": "is not null"
        }

        return operator_map.get(operator, "=")

    def _format_value(self, value: Any) -> str:
        """
        Format a value for use in a ConnectWise Manage condition.

        Args:
            value: Value to format

        Returns:
            Formatted value
        """
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif value is None:
            return "null"
        elif isinstance(value, list):
            formatted_values = [self._format_value(v) for v in value]
            return f"[{','.join(formatted_values)}]"
        else:
            return str(value)

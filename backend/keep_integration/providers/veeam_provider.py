"""
Veeam Provider for Keep.dev

This module implements a Keep.dev provider for Veeam Backup & Replication,
allowing Keep to interact with Veeam backup jobs and sessions.
"""

from typing import Any, Dict, List, Optional
import logging
import httpx
import base64
from datetime import datetime, timedelta

from keep.providers.base.base_provider import BaseProvider
from keep.providers.models.provider_config import ProviderConfig

logger = logging.getLogger(__name__)

class VeeamProvider(BaseProvider):
    """
    Veeam provider for Keep.dev.

    This provider allows Keep to:
    1. Query backup jobs and sessions from Veeam
    2. Monitor backup job status
    3. Sync alerts between Keep and Veeam
    """

    PROVIDER_DISPLAY_NAME = "Veeam Backup & Replication"
    PROVIDER_CATEGORY = ["Backup", "Disaster Recovery"]
    PROVIDER_TAGS = ["msp", "backup", "dr"]
    PROVIDER_DESCRIPTION = "Veeam Backup & Replication is a backup and disaster recovery solution."
    FINGERPRINT_FIELDS = ["id", "name"]

    def __init__(self, provider_id, config):
        super().__init__(provider_id, config)
        self.client = None
        self.token = None
        self.token_expiry = None
        self._init_client()

    def _init_client(self):
        """Initialize the Veeam client."""
        try:
            auth_config = self.config.authentication
            self.username = auth_config.get("username")
            self.password = auth_config.get("password")
            self.base_url = auth_config.get("base_url")

            # Validate required configuration
            if not all([self.username, self.password, self.base_url]):
                logger.error("Missing required Veeam authentication configuration")
                return

            # Initialize HTTP client
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                verify=False,  # Veeam often uses self-signed certificates
                timeout=30.0
            )
            logger.info(f"Veeam client initialized")
        except Exception as e:
            logger.error(f"Error initializing Veeam client: {e}")
            self.client = None

    async def _get_token(self):
        """
        Get an authentication token from Veeam.

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("Veeam client not initialized")
            return False

        # Check if we already have a valid token
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return True

        try:
            # Prepare authentication headers
            auth_string = f"{self.username}:{self.password}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()

            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Content-Type": "application/x-www-form-urlencoded",
                "x-api-version": "1.0-rev1"
            }

            # Make API request
            response = await self.client.post(
                "/api/oauth2/token",
                headers=headers,
                data="grant_type=password&username=&password="
            )
            response.raise_for_status()

            # Parse response
            data = response.json()
            self.token = data.get("access_token")
            expires_in = data.get("expires_in", 900)  # Default to 15 minutes
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)

            # Update client headers
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "x-api-version": "1.0-rev1"
            })

            return True
        except Exception as e:
            logger.error(f"Error getting Veeam token: {e}")
            self.token = None
            self.token_expiry = None
            return False

    async def query(self, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query backup jobs and sessions from Veeam.

        Args:
            query_params: Parameters for the query
                - query_type: Type of query (jobs, sessions, repositories, vms, protected_vms)
                - filters: Dictionary of filters
                - limit: Maximum number of results (default: 100)
                - offset: Pagination offset
                - client_id: Optional client ID to filter results

        Returns:
            List of items matching the query
        """
        if not await self._get_token():
            logger.error("Failed to get Veeam token")
            return []

        try:
            # Extract query parameters
            query_type = query_params.get("query_type", "jobs")
            filters = query_params.get("filters", {})
            limit = query_params.get("limit", 100)
            offset = query_params.get("offset", 0)
            client_id = query_params.get("client_id")

            # If client_id is provided, get the client-specific filters
            if client_id:
                client_filters = await self._get_client_filters(client_id)
                if client_filters:
                    # Merge client filters with existing filters
                    filters.update(client_filters)

            # Build query parameters
            params = {
                "limit": limit,
                "offset": offset
            }

            # Add filters if provided
            if filters:
                for key, value in filters.items():
                    params[key] = value

            # Determine endpoint based on query type
            if query_type == "jobs":
                endpoint = "/api/v1/jobs"
            elif query_type == "sessions":
                endpoint = "/api/v1/sessions"
            elif query_type == "repositories":
                endpoint = "/api/v1/backupInfrastructure/repositories"
            elif query_type == "vms":
                endpoint = "/api/v1/inventory/vms"
            elif query_type == "protected_vms":
                endpoint = "/api/v1/inventory/protectedVms"
            else:
                logger.error(f"Unsupported query type: {query_type}")
                return []

            # Make API request
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()

            # Parse response
            data = response.json()

            # Extract items based on query type
            if query_type == "jobs":
                items = data.get("data", [])
                return [self._transform_job_to_alert(job) for job in items]
            elif query_type == "sessions":
                items = data.get("data", [])
                return [self._transform_session_to_alert(session) for session in items]
            elif query_type == "repositories":
                items = data.get("data", [])
                return items
            elif query_type == "vms":
                items = data.get("data", [])
                return items
            elif query_type == "protected_vms":
                items = data.get("data", [])
                return items

            return []
        except Exception as e:
            logger.error(f"Error querying Veeam: {e}")
            return []

    async def notify(self, notification_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Veeam jobs.

        Args:
            notification_params: Parameters for the action
                - action: Action to perform (start, stop, retry)
                - job_id: ID of the job

        Returns:
            Result of the action
        """
        if not await self._get_token():
            logger.error("Failed to get Veeam token")
            return {"success": False, "message": "Failed to authenticate"}

        try:
            # Extract parameters
            action = notification_params.get("action")
            job_id = notification_params.get("job_id")

            if not action or not job_id:
                return {"success": False, "message": "Action and job_id are required"}

            # Perform action based on type
            if action == "start":
                return await self._start_job(job_id)
            elif action == "stop":
                return await self._stop_job(job_id)
            elif action == "retry":
                return await self._retry_job(job_id)
            else:
                return {"success": False, "message": f"Unsupported action: {action}"}
        except Exception as e:
            logger.error(f"Error in Veeam notify operation: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    async def _start_job(self, job_id: str) -> Dict[str, Any]:
        """
        Start a backup job.

        Args:
            job_id: ID of the job to start

        Returns:
            Result of the operation
        """
        endpoint = f"/api/v1/jobs/{job_id}/start"

        response = await self.client.post(endpoint)
        response.raise_for_status()

        return {
            "success": True,
            "message": "Job started successfully",
            "task_id": response.json().get("taskId")
        }

    async def _stop_job(self, job_id: str) -> Dict[str, Any]:
        """
        Stop a backup job.

        Args:
            job_id: ID of the job to stop

        Returns:
            Result of the operation
        """
        endpoint = f"/api/v1/jobs/{job_id}/stop"

        response = await self.client.post(endpoint)
        response.raise_for_status()

        return {
            "success": True,
            "message": "Job stopped successfully"
        }

    async def _get_client_filters(self, client_id: str) -> Dict[str, Any]:
        """
        Get Veeam-specific filters for a client.

        This method retrieves the mapping between a client ID and Veeam-specific
        filters such as VM names, job names, etc.

        Args:
            client_id: MSPAlwaysOn client ID

        Returns:
            Dictionary of Veeam-specific filters
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

            # Get client name and metadata containing Veeam-specific filters if available
            client_name = client.name
            metadata = client.metadata or {}
            veeam_filters = metadata.get("veeam_filters", {})

            # If we have direct filter mappings in metadata, use them
            if veeam_filters:
                return veeam_filters

            # Otherwise, use a name-based filter as fallback
            return {
                "name": client_name  # This will filter jobs/VMs by name containing the client name
            }
        except Exception as e:
            logger.error(f"Error getting client filters for Veeam: {e}")
            return {}

    async def _retry_job(self, job_id: str) -> Dict[str, Any]:
        """
        Retry a failed backup job.

        Args:
            job_id: ID of the job to retry

        Returns:
            Result of the operation
        """
        endpoint = f"/api/v1/jobs/{job_id}/retry"

        response = await self.client.post(endpoint)
        response.raise_for_status()

        return {
            "success": True,
            "message": "Job retry initiated successfully",
            "task_id": response.json().get("taskId")
        }

    def _transform_job_to_alert(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a Veeam job to a Keep alert format.

        Args:
            job: Veeam job

        Returns:
            Keep alert
        """
        # Map job status to alert severity
        severity_map = {
            "Success": "info",
            "Warning": "warning",
            "Failed": "critical",
            "Running": "info",
            "Idle": "info"
        }

        # Map job status to alert status
        status_map = {
            "Success": "resolved",
            "Warning": "firing",
            "Failed": "firing",
            "Running": "firing",
            "Idle": "resolved"
        }

        # Get job status
        job_status = job.get("lastResult", "Unknown")

        # Map to Keep alert
        return {
            "id": str(job.get("id")),
            "name": f"Veeam Job: {job.get('name', 'Unknown Job')}",
            "description": job.get("description", ""),
            "source": "veeam",
            "severity": severity_map.get(job_status, "info"),
            "status": status_map.get(job_status, "firing"),
            "lastReceived": job.get("lastRun", datetime.now().isoformat()),
            "fingerprint": f"veeam-job-{job.get('id')}",
            "labels": {
                "job_name": job.get("name", "Unknown"),
                "job_type": job.get("type", "Unknown"),
                "schedule_enabled": str(job.get("scheduleEnabled", False)).lower(),
                "last_result": job_status,
                "repository": job.get("repository", {}).get("name", "Unknown") if job.get("repository") else "Unknown"
            },
            "annotations": {
                "job_id": str(job.get("id")),
                "schedule_enabled": str(job.get("scheduleEnabled", False)).lower(),
                "last_run": job.get("lastRun", ""),
                "next_run": job.get("nextRun", "")
            },
            "raw_data": job
        }

    def _transform_session_to_alert(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a Veeam session to a Keep alert format.

        Args:
            session: Veeam session

        Returns:
            Keep alert
        """
        # Map session status to alert severity
        severity_map = {
            "Success": "info",
            "Warning": "warning",
            "Failed": "critical",
            "Running": "info",
            "Idle": "info"
        }

        # Map session status to alert status
        status_map = {
            "Success": "resolved",
            "Warning": "firing",
            "Failed": "firing",
            "Running": "firing",
            "Idle": "resolved"
        }

        # Get session status
        session_status = session.get("result", "Unknown")

        # Map to Keep alert
        return {
            "id": str(session.get("id")),
            "name": f"Veeam Session: {session.get('jobName', 'Unknown Job')}",
            "description": f"Backup session for job {session.get('jobName', 'Unknown Job')}",
            "source": "veeam",
            "severity": severity_map.get(session_status, "info"),
            "status": status_map.get(session_status, "firing"),
            "lastReceived": session.get("creationTime", datetime.now().isoformat()),
            "fingerprint": f"veeam-session-{session.get('id')}",
            "labels": {
                "job_name": session.get("jobName", "Unknown"),
                "result": session_status,
                "progress": str(session.get("progress", 0)),
                "is_retry": str(session.get("isRetry", False)).lower()
            },
            "annotations": {
                "session_id": str(session.get("id")),
                "job_id": str(session.get("jobId")),
                "creation_time": session.get("creationTime", ""),
                "end_time": session.get("endTime", "")
            },
            "raw_data": session
        }

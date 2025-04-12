"""
Tests for the ConnectWise Manage provider.
"""

import os
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from keep.providers.models.provider_config import ProviderConfig
from keep_integration.providers.connectwise_provider import ConnectWiseManageProvider

# Test data
TEST_PROVIDER_ID = "test-connectwise-provider"
TEST_CONFIG = {
    "authentication": {
        "company_id": "test_company",
        "public_key": "test_public_key",
        "private_key": "test_private_key",
        "client_id": "test_client_id",
        "base_url": "https://test.connectwisedev.com/v4_6_release/apis/3.0"
    }
}

TEST_TICKET = {
    "id": 123,
    "summary": "Test Ticket",
    "initialDescription": "This is a test ticket",
    "board": {"id": 1, "name": "Service Board"},
    "company": {"id": 2, "name": "Test Company"},
    "status": {"id": 1, "name": "New"},
    "priority": {"id": 2, "name": "High"},
    "owner": {"id": 3, "identifier": "jdoe"},
    "_info": {"lastUpdated": "2023-04-12T12:34:56Z"}
}

@pytest.fixture
def provider_config():
    """Create a provider config for testing."""
    return ProviderConfig(
        provider_id=TEST_PROVIDER_ID,
        **TEST_CONFIG
    )

@pytest.fixture
def provider(provider_config):
    """Create a ConnectWise Manage provider for testing."""
    provider = ConnectWiseManageProvider(TEST_PROVIDER_ID, provider_config)
    # Mock the HTTP client
    provider.client = AsyncMock()
    return provider

@pytest.mark.asyncio
async def test_query(provider):
    """Test querying tickets from ConnectWise Manage."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = [TEST_TICKET]
    provider.client.get.return_value = mock_response

    # Call the query method
    result = await provider.query({
        "conditions": [
            {"field": "status", "operator": "equals", "value": "New"}
        ],
        "page": 1,
        "page_size": 10
    })

    # Verify the result
    assert len(result) == 1
    assert result[0]["id"] == str(TEST_TICKET["id"])
    assert result[0]["name"] == TEST_TICKET["summary"]
    assert result[0]["source"] == "connectwise-manage"
    assert result[0]["severity"] == "critical"  # New status maps to critical
    assert result[0]["status"] == "firing"
    assert result[0]["fingerprint"] == f"connectwise-manage-{TEST_TICKET['id']}"

    # Verify the API call
    provider.client.get.assert_called_once()
    args, kwargs = provider.client.get.call_args
    assert args[0] == "/service/tickets"
    assert "conditions" in kwargs["params"]
    assert kwargs["params"]["page"] == 1
    assert kwargs["params"]["pageSize"] == 10

@pytest.mark.asyncio
async def test_create_ticket(provider):
    """Test creating a ticket in ConnectWise Manage."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = TEST_TICKET
    provider.client.post.return_value = mock_response

    # Call the notify method
    result = await provider.notify({
        "summary": "Test Ticket",
        "description": "This is a test ticket",
        "board_id": 1,
        "company_id": 2,
        "status_id": 1,
        "priority_id": 2
    })

    # Verify the result
    assert result["success"] is True
    assert result["message"] == "Ticket created successfully"
    assert result["ticket"] == TEST_TICKET
    assert result["ticket_id"] == TEST_TICKET["id"]

    # Verify the API call
    provider.client.post.assert_called_once()
    args, kwargs = provider.client.post.call_args
    assert args[0] == "/service/tickets"
    assert kwargs["json"]["summary"] == "Test Ticket"
    assert kwargs["json"]["initialDescription"] == "This is a test ticket"
    assert kwargs["json"]["board"]["id"] == 1
    assert kwargs["json"]["company"]["id"] == 2
    assert kwargs["json"]["status"]["id"] == 1
    assert kwargs["json"]["priority"]["id"] == 2

@pytest.mark.asyncio
async def test_update_ticket(provider):
    """Test updating a ticket in ConnectWise Manage."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = TEST_TICKET
    provider.client.patch.return_value = mock_response

    # Call the notify method
    result = await provider.notify({
        "ticket_id": 123,
        "summary": "Updated Ticket",
        "status_id": 2
    })

    # Verify the result
    assert result["success"] is True
    assert result["message"] == "Ticket updated successfully"
    assert result["ticket"] == TEST_TICKET
    assert result["ticket_id"] == TEST_TICKET["id"]

    # Verify the API call
    provider.client.patch.assert_called_once()
    args, kwargs = provider.client.patch.call_args
    assert args[0] == "/service/tickets/123"
    assert kwargs["json"]["summary"] == "Updated Ticket"
    assert kwargs["json"]["status"]["id"] == 2

@pytest.mark.asyncio
async def test_add_ticket_note(provider):
    """Test adding a note to a ticket in ConnectWise Manage."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 456, "text": "Test note"}
    provider.client.post.return_value = mock_response

    # Call the _add_ticket_note method
    result = await provider._add_ticket_note(123, "Test note", internal=True)

    # Verify the result
    assert result["success"] is True
    assert result["message"] == "Note added successfully"
    assert result["note"]["id"] == 456
    assert result["note"]["text"] == "Test note"

    # Verify the API call
    provider.client.post.assert_called_once()
    args, kwargs = provider.client.post.call_args
    assert args[0] == "/service/tickets/123/notes"
    assert kwargs["json"]["text"] == "Test note"
    assert kwargs["json"]["internalAnalysisFlag"] is True
    assert kwargs["json"]["externalFlag"] is False

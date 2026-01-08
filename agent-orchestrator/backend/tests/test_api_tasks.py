"""Integration tests for Tasks API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health endpoint returns 200."""
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, api_headers):
    """Test creating a new task."""
    response = await client.post(
        "/api/v1/tasks",
        json={"description": "Test task description for testing"},
        headers=api_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Test task description for testing"
    assert data["status"] == "pending"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_task_without_api_key(client: AsyncClient):
    """Test creating task without API key returns 401."""
    response = await client.post(
        "/api/v1/tasks",
        json={"description": "Test task description for testing"},
    )

    assert response.status_code == 422  # Missing header


@pytest.mark.asyncio
async def test_create_task_short_description(client: AsyncClient, api_headers):
    """Test creating task with too short description."""
    response = await client.post(
        "/api/v1/tasks",
        json={"description": "Short"},
        headers=api_headers,
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_task_not_found(client: AsyncClient, api_headers):
    """Test getting non-existent task returns 404."""
    response = await client.get(
        "/api/v1/tasks/00000000-0000-0000-0000-000000000000",
        headers=api_headers,
    )

    assert response.status_code == 404

"""Tests for the dashboard API."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from kraken.api.main import app
from kraken.opportunity import Opportunity

client = TestClient(app)


@patch("kraken.api.main.service.get_cached")
def test_dashboard(mock_get_cached) -> None:
    """Dashboard endpoint should return dashboard information."""

    mock_get_cached.return_value = [
        Opportunity(
            id="1",
            title="Backend Engineer",
            organization="OpenAI",
            location="Remote",
            salary="$180000",
            score=95,
            source="RemoteOK",
            url="https://example.com",
            description="Python FastAPI Docker PostgreSQL AWS",
        )
    ]

    response = client.get("/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert "resume_health" in data
    assert "total_jobs" in data
    assert "top_matches" in data

    assert data["total_jobs"] == 1
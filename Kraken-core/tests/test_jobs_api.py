"""Tests for the jobs API endpoint."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from kraken.api.main import app
from kraken.opportunity import Opportunity

client = TestClient(app)


@patch("kraken.api.main.service.get_cached")
def test_get_jobs(mock_get_cached) -> None:
    """GET /jobs should return cached opportunities."""

    mock_get_cached.return_value = [
        Opportunity(
            id="1",
            title="Software Engineer",
            source="RemoteOK",
            url="https://example.com",
            organization="OpenAI",
            location="Remote",
            salary="$120000",
            score=100,
            description="AI Engineer",
        )
    ]

    response = client.get("/jobs")

    assert response.status_code == 200

    jobs = response.json()

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Software Engineer"
    assert jobs[0]["organization"] == "OpenAI"
    assert jobs[0]["score"] == 100
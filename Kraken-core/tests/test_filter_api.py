"""Tests for the filter API."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from kraken.api.main import app
from kraken.opportunity import Opportunity

client = TestClient(app)


@patch("kraken.collectors.remoteok.RemoteOKCollector.collect")
def test_filter_by_company_and_score(mock_collect) -> None:
    mock_collect.return_value = [
        Opportunity(
            id="1",
            title="Python Developer",
            source="RemoteOK",
            url="https://example.com/1",
            organization="OpenAI",
            location="Remote",
            description="Python backend",
            salary="$120000",
        ),
        Opportunity(
            id="2",
            title="React Developer",
            source="RemoteOK",
            url="https://example.com/2",
            organization="Meta",
            location="Remote",
            description="Frontend React",
            salary="$90000",
        ),
    ]

    response = client.get("/jobs?company=OpenAI&min_score=100")

    assert response.status_code == 200

    jobs = response.json()

    assert len(jobs) == 1
    assert jobs[0]["organization"] == "OpenAI"
    assert jobs[0]["score"] == 100
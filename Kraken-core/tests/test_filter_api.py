"""Tests for filtering opportunities."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from kraken.api.main import app
from kraken.opportunity import Opportunity

client = TestClient(app)


@patch("kraken.api.main.service.get_cached")
def test_filter_by_company_and_score(mock_get_cached) -> None:
    """Filtering by company and score should work."""

    mock_get_cached.return_value = [
        Opportunity(
            id="1",
            title="Python Developer",
            source="RemoteOK",
            url="https://example.com/1",
            organization="OpenAI",
            location="Remote",
            description="Python backend",
            salary="$120000",
            score=100,
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
            score=40,
        ),
    ]

    response = client.get("/jobs?company=OpenAI&min_score=100")

    assert response.status_code == 200

    jobs = response.json()

    assert len(jobs) == 1
    assert jobs[0]["organization"] == "OpenAI"
    assert jobs[0]["opportunity_score"] == 100

    assert "personal_match" in jobs[0]
    assert "insights" in jobs[0]
    assert "why_this_matches" in jobs[0]
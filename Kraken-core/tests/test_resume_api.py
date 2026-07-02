"""Tests for the resume analysis API."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from kraken.api.main import app
from kraken.opportunity import Opportunity

client = TestClient(app)


@patch("kraken.api.main.service.get_cached")
def test_resume_analysis(mock_get_cached) -> None:
    """Resume analysis should return extracted skills and ranked matches."""

    mock_get_cached.return_value = [
        Opportunity(
            id="1",
            title="Backend Engineer",
            organization="OpenAI",
            location="Remote",
            salary="$180000",
            score=95,
            source="RemoteOK",
            url="https://example.com/job",
            description="Python FastAPI Docker PostgreSQL AWS",
        ),
        Opportunity(
            id="2",
            title="Marketing Manager",
            organization="Example Ltd",
            location="Accra",
            salary="$50000",
            score=50,
            source="RemoteOK",
            url="https://example.com/job2",
            description="Marketing Sales Communication",
        ),
    ]

    response = client.post(
        "/resume/analyze",
        json={
            "resume": "Python FastAPI Docker PostgreSQL"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "skills" in data
    assert "top_matches" in data

    assert "python" in data["skills"]
    assert "docker" in data["skills"]

    assert len(data["top_matches"]) == 2

    assert data["top_matches"][0]["title"] == "Backend Engineer"
    assert data["top_matches"][0]["resume_match"] == 80
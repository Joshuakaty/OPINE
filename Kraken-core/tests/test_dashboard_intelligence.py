"""Tests for the intelligent dashboard."""

from kraken.dashboard import Dashboard
from kraken.opportunity import Opportunity
from kraken.resume_profile import ResumeProfile


def test_dashboard_intelligence() -> None:
    """Dashboard should expose intelligent summary information."""

    profile = ResumeProfile()

    profile.update(
        """
        Python
        FastAPI
        Docker
        PostgreSQL
        """
    )

    opportunities = [
        Opportunity(
            id="1",
            title="Backend Engineer",
            organization="OpenAI",
            location="Remote",
            salary="$180000",
            score=95,
            source="RemoteOK",
            url="https://example.com/1",
            description="""
            Python
            FastAPI
            Docker
            PostgreSQL
            AWS
            """,
        ),
        Opportunity(
            id="2",
            title="React Developer",
            organization="Meta",
            location="Remote",
            salary="$140000",
            score=70,
            source="RemoteOK",
            url="https://example.com/2",
            description="""
            React
            JavaScript
            CSS
            """,
        ),
    ]

    dashboard = Dashboard()

    data = dashboard.build(
        profile,
        opportunities,
    )

    assert data["resume_health"] == 40
    assert data["total_jobs"] == 2

    # Backend Engineer matches at 80% because AWS is missing.
    assert data["excellent_matches"] == 0
    assert data["average_match"] == 40

    assert isinstance(data["learning_recommendations"], list)
    assert len(data["top_matches"]) == 2

    assert data["top_matches"][0]["title"] == "Backend Engineer"
    assert data["top_matches"][0]["match"] == 80
"""Tests for the dashboard."""

from kraken.dashboard import Dashboard
from kraken.opportunity import Opportunity
from kraken.resume_profile import ResumeProfile


def test_dashboard_build() -> None:
    """Dashboard should summarize opportunities."""

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
            url="https://example.com/job",
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
            title="Marketing Manager",
            organization="Example Ltd",
            location="Accra",
            salary="$50000",
            score=40,
            source="RemoteOK",
            url="https://example.com/job2",
            description="""
            Marketing
            Sales
            Communication
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

    assert len(data["top_matches"]) == 2

    assert data["top_matches"][0]["title"] == "Backend Engineer"
    assert data["top_matches"][0]["match"] == 80
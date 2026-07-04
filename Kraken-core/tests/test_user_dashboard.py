"""Tests for user dashboards."""

from kraken.dashboard import Dashboard
from kraken.opportunity import Opportunity
from kraken.users.user import User


def test_user_dashboard() -> None:
    """A user should receive a personalized dashboard."""

    user = User(
        id="1",
        name="Joshua",
        email="joshua@example.com",
    )

    user.update_resume(
        """
        Python
        FastAPI
        Docker
        PostgreSQL
        """
    )

    dashboard = Dashboard()

    opportunities = [
        Opportunity(
            id="1",
            title="Backend Engineer",
            organization="OpenAI",
            location="Remote",
            salary="$180000",
            score=95,
            source="RemoteOK",
            url="https://example.com",
            description="""
            Python
            FastAPI
            Docker
            PostgreSQL
            AWS
            """,
        )
    ]

    data = dashboard.build(
        user.resume_profile,
        opportunities,
    )

    assert data["resume_health"] == 40
    assert data["total_jobs"] == 1
    assert data["average_match"] == 80
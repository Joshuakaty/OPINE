"""Tests for learning recommendations."""

from kraken.learning import LearningRecommender
from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile


def test_learning_recommendations() -> None:
    """Missing skills should become learning recommendations."""

    profile = UserProfile(
        name="Joshua",
        skills=["Python", "FastAPI"],
    )

    opportunity = Opportunity(
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
    )

    recommender = LearningRecommender()

    recommendations = recommender.recommend(
        profile,
        opportunity,
    )

    assert "docker" in recommendations
    assert "postgresql" in recommendations
    assert "aws" in recommendations

    assert "python" not in recommendations
    assert "fastapi" not in recommendations


def test_no_learning_needed() -> None:
    """No recommendations should be returned if nothing is missing."""

    profile = UserProfile(
        name="Joshua",
        skills=[
            "Python",
            "FastAPI",
            "Docker",
            "PostgreSQL",
            "AWS",
        ],
    )

    opportunity = Opportunity(
        id="2",
        title="Backend Engineer",
        organization="OpenAI",
        location="Remote",
        salary="$180000",
        score=95,
        source="RemoteOK",
        url="https://example.com/job2",
        description="""
        Python
        FastAPI
        Docker
        PostgreSQL
        AWS
        """,
    )

    recommender = LearningRecommender()

    assert recommender.recommend(profile, opportunity) == []
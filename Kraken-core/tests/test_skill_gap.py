"""Tests for skill gap analysis."""

from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile
from kraken.skill_gap import SkillGapAnalyzer


def test_missing_skills() -> None:
    """Missing skills should be identified correctly."""

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
        description=(
            "Python FastAPI Docker PostgreSQL AWS"
        ),
    )

    analyzer = SkillGapAnalyzer()

    missing = analyzer.missing_skills(
        profile,
        opportunity,
    )

    assert "docker" in missing
    assert "postgresql" in missing
    assert "aws" in missing

    assert "python" not in missing
    assert "fastapi" not in missing


def test_no_missing_skills() -> None:
    """No skills should be missing if the user has everything."""

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
        title="Python Engineer",
        organization="OpenAI",
        location="Remote",
        salary="$180000",
        score=95,
        source="RemoteOK",
        url="https://example.com/job2",
        description=(
            "Python FastAPI Docker PostgreSQL AWS"
        ),
    )

    analyzer = SkillGapAnalyzer()

    assert analyzer.missing_skills(profile, opportunity) == []
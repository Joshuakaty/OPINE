"""Tests for the resume matcher."""

from kraken.opportunity import Opportunity
from kraken.resume_matcher import ResumeMatcher


def test_resume_match_score() -> None:
    """Resume should match most required skills."""

    resume = """
    Python
    FastAPI
    Docker
    PostgreSQL
    """

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

    matcher = ResumeMatcher()

    score = matcher.match(
        resume,
        opportunity,
    )

    assert score == 80


def test_resume_no_match() -> None:
    """Unrelated resumes should receive zero."""

    resume = """
    Marketing
    Sales
    Management
    """

    opportunity = Opportunity(
        id="2",
        title="Python Developer",
        organization="OpenAI",
        location="Remote",
        salary="$150000",
        score=90,
        source="RemoteOK",
        url="https://example.com/job2",
        description="""
        Python
        FastAPI
        Docker
        AWS
        """,
    )

    matcher = ResumeMatcher()

    score = matcher.match(
        resume,
        opportunity,
    )

    assert score == 0
    
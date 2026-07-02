"""Tests for the skill extractor."""

from kraken.opportunity import Opportunity
from kraken.skills import SkillExtractor


def test_extract_skills() -> None:
    """Known skills should be extracted from an opportunity."""

    opportunity = Opportunity(
        id="1",
        title="Senior Python Backend Engineer",
        organization="OpenAI",
        location="Remote",
        salary="$180000",
        score=95,
        source="RemoteOK",
        url="https://example.com/job",
        description=(
            "Build APIs using FastAPI, Docker, "
            "PostgreSQL and AWS."
        ),
    )

    extractor = SkillExtractor()

    skills = extractor.extract(opportunity)

    assert "python" in skills
    assert "fastapi" in skills
    assert "docker" in skills
    assert "postgresql" in skills
    assert "aws" in skills


def test_extract_no_skills() -> None:
    """Jobs without known skills should return an empty list."""

    opportunity = Opportunity(
        id="2",
        title="Office Administrator",
        organization="Example Ltd",
        location="Accra",
        salary="",
        score=20,
        source="RemoteOK",
        url="https://example.com/job2",
        description="General office administration duties.",
    )

    extractor = SkillExtractor()

    assert extractor.extract(opportunity) == []
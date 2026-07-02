"""Tests for opportunity deduplication."""

from kraken.deduplication import deduplicate
from kraken.opportunity import Opportunity


def test_remove_duplicate_opportunities() -> None:
    """Duplicate opportunities should be removed."""

    opportunities = [
        Opportunity(
            id="1",
            title="Python Developer",
            organization="OpenAI",
            location="Remote",
            salary="$120000",
            score=100,
            source="RemoteOK",
            url="https://example.com/job1",
            description="Backend Python",
        ),
        Opportunity(
            id="1",
            title="Python Developer",
            organization="OpenAI",
            location="Remote",
            salary="$120000",
            score=100,
            source="Arbeitnow",
            url="https://example.com/job1",
            description="Backend Python",
        ),
        Opportunity(
            id="2",
            title="Backend Engineer",
            organization="Meta",
            location="Remote",
            salary="$90000",
            score=90,
            source="RemoteOK",
            url="https://example.com/job2",
            description="Backend Engineer",
        ),
    ]

    unique = deduplicate(opportunities)

    assert len(unique) == 2
    assert unique[0].id == "1"
    assert unique[1].id == "2"
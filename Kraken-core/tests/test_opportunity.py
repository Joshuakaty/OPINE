"""Tests for the Opportunity model."""

from kraken.opportunity import Opportunity


def test_create_opportunity() -> None:
    opportunity = Opportunity(
        id="1",
        title="Software Engineer",
        source="Sample",
        url="https://example.com/job/1",
    )

    assert opportunity.id == "1"
    assert opportunity.title == "Software Engineer"
    assert opportunity.source == "Sample"
    assert opportunity.url == "https://example.com/job/1"
    assert opportunity.score == 0
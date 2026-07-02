"""Tests for opportunity ranking."""

from kraken.opportunity import Opportunity
from kraken.ranking import OpportunityRanker


def test_rank_opportunities() -> None:
    high = Opportunity(
        id="1",
        title="High",
        source="Sample",
        url="https://example.com/1",
        score=90,
    )

    low = Opportunity(
        id="2",
        title="Low",
        source="Sample",
        url="https://example.com/2",
        score=40,
    )

    ranker = OpportunityRanker()

    ranked = ranker.rank([low, high])

    assert ranked[0].score == 90
    assert ranked[1].score == 40
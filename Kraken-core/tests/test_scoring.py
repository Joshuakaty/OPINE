"""Tests for opportunity scoring."""

from kraken.opportunity import Opportunity
from kraken.scoring import OpportunityScorer


def test_score_remote_job_with_salary() -> None:
    opportunity = Opportunity(
        id="1",
        title="Software Engineer",
        source="Sample",
        url="https://example.com",
        location="Remote",
        organization="OpenAI",
        description="AI engineering role",
        salary="$120000",
    )

    scorer = OpportunityScorer()

    assert scorer.score(opportunity) == 100
    assert opportunity.score == 100
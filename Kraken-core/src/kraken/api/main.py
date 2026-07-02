"""FastAPI application for OPINE."""

from fastapi import FastAPI

from kraken.collectors.jobs import JobsCollector
from kraken.ranking import OpportunityRanker
from kraken.scoring import OpportunityScorer

app = FastAPI(
    title="OPINE API",
    version="0.4.0",
    description="Opportunity Intelligence Engine API",
)


@app.get("/")
def root() -> dict[str, str]:
    """Health endpoint."""
    return {
        "name": "OPINE API",
        "status": "running",
        "engine": "Kraken",
    }


@app.get("/jobs")
def get_jobs() -> list[dict]:
    """Return ranked opportunities."""

    collector = JobsCollector()
    scorer = OpportunityScorer()
    ranker = OpportunityRanker()

    opportunities = collector.collect()

    for opportunity in opportunities:
        scorer.score(opportunity)

    opportunities = ranker.rank(opportunities)

    return [
        {
            "id": opportunity.id,
            "title": opportunity.title,
            "organization": opportunity.organization,
            "location": opportunity.location,
            "salary": opportunity.salary,
            "score": opportunity.score,
        }
        for opportunity in opportunities
    ]
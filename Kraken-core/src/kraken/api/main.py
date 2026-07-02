"""FastAPI application for OPINE."""

from fastapi import FastAPI

from kraken.intelligence import OpportunityIntelligence
from kraken.services.database_service import DatabaseService

app = FastAPI(
    title="OPINE API",
    version="0.7.0",
    description="Opportunity Intelligence Engine API",
)

service = DatabaseService()
intelligence = OpportunityIntelligence()


@app.get("/")
def root() -> dict[str, str]:
    """Health endpoint."""
    return {
        "name": "OPINE API",
        "status": "running",
        "engine": "Kraken",
    }


@app.post("/refresh")
def refresh_jobs() -> dict[str, int | str]:
    """Refresh the local opportunity database."""

    count = service.refresh_and_cache()

    return {
        "status": "success",
        "jobs_collected": count,
    }


@app.get("/jobs")
def get_jobs(
    q: str | None = None,
    location: str | None = None,
    company: str | None = None,
    min_score: int | None = None,
) -> list[dict]:
    """Return cached ranked opportunities."""

    opportunities = service.get_cached()

    # Search filter.
    if q:
        query = q.lower()
        opportunities = [
            opportunity
            for opportunity in opportunities
            if query in opportunity.title.lower()
            or query in opportunity.description.lower()
            or query in opportunity.organization.lower()
        ]

    # Location filter.
    if location:
        opportunities = [
            opportunity
            for opportunity in opportunities
            if location.lower() in opportunity.location.lower()
        ]

    # Company filter.
    if company:
        opportunities = [
            opportunity
            for opportunity in opportunities
            if company.lower() in opportunity.organization.lower()
        ]

    # Minimum score filter.
    if min_score is not None:
        opportunities = [
            opportunity
            for opportunity in opportunities
            if opportunity.score >= min_score
        ]

    return [
        {
            "id": opportunity.id,
            "title": opportunity.title,
            "organization": opportunity.organization,
            "location": opportunity.location,
            "salary": opportunity.salary,
            "score": opportunity.score,
            "source": opportunity.source,
            "insights": intelligence.analyze(opportunity),
        }
        for opportunity in opportunities
    ]
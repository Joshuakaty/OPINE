"""Job API response schemas."""

from __future__ import annotations

from pydantic import BaseModel


class JobResponse(BaseModel):
    """A job returned by the OPINE API."""

    id: str
    title: str
    organization: str
    location: str
    salary: str
    opportunity_score: int
    personal_match: int
    source: str
    insights: list[str]
    why_this_matches: list[str]
"""Resume API response schemas."""

from __future__ import annotations

from pydantic import BaseModel


class ResumeMatch(BaseModel):
    """One resume match."""

    title: str
    organization: str
    resume_match: int


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis response."""

    skills: list[str]
    top_matches: list[ResumeMatch]
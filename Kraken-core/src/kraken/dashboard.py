"""Dashboard generation for OPINE."""

from __future__ import annotations

from kraken.opportunity import Opportunity
from kraken.resume_health import ResumeHealth
from kraken.resume_matcher import ResumeMatcher
from kraken.resume_profile import ResumeProfile


class Dashboard:
    """Generate a personalized dashboard."""

    def __init__(self) -> None:
        self.health = ResumeHealth()
        self.matcher = ResumeMatcher()

    def build(
        self,
        profile: ResumeProfile,
        opportunities: list[Opportunity],
    ) -> dict:
        """Build a dashboard from a profile and opportunities."""

        resume_score = self.health.score(profile.resume_text)

        matches = []

        for opportunity in opportunities:
            matches.append(
                {
                    "title": opportunity.title,
                    "organization": opportunity.organization,
                    "match": self.matcher.match(
                        profile.resume_text,
                        opportunity,
                    ),
                }
            )

        matches.sort(
            key=lambda item: item["match"],
            reverse=True,
        )

        return {
            "resume_health": resume_score,
            "total_jobs": len(opportunities),
            "top_matches": matches[:5],
        }
"""Opportunity Intelligence Engine."""

from __future__ import annotations

from kraken.opportunity import Opportunity


class OpportunityIntelligence:
    """Generate human-readable insights for opportunities."""

    AI_COMPANIES = {
        "openai",
        "anthropic",
        "google deepmind",
        "mistral ai",
        "cohere",
        "hugging face",
    }

    def analyze(self, opportunity: Opportunity) -> list[str]:
        """Return intelligence insights for an opportunity."""

        insights: list[str] = []

        # Remote jobs
        if "remote" in opportunity.location.lower():
            insights.append("Remote opportunity")

        # Python jobs
        if "python" in (
            opportunity.title + " " + opportunity.description
        ).lower():
            insights.append("Python role")

        # High salary
        if opportunity.salary:
            insights.append("Salary information available")

        # AI company
        if opportunity.organization.lower() in self.AI_COMPANIES:
            insights.append("AI company")

        if not insights:
            insights.append("General opportunity")

        return insights
"""Opportunity ranking."""

from kraken.opportunity import Opportunity


class OpportunityRanker:
    """Ranks opportunities by score."""

    def rank(self, opportunities: list[Opportunity]) -> list[Opportunity]:
        """Return opportunities sorted from highest to lowest score."""
        return sorted(
            opportunities,
            key=lambda opportunity: opportunity.score,
            reverse=True,
        )
"""Opportunity scoring."""

from kraken.opportunity import Opportunity


class OpportunityScorer:
    """Scores opportunities."""

    def score(self, opportunity: Opportunity) -> int:
        score = 0

        if opportunity.salary:
            score += 40

        if opportunity.location.lower() == "remote":
            score += 20

        if opportunity.organization:
            score += 20

        if opportunity.description:
            score += 20

        opportunity.score = score

        return score
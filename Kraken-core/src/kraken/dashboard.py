"""Dashboard generation for OPINE."""

from __future__ import annotations

from kraken.learning import LearningRecommender
from kraken.opportunity import Opportunity
from kraken.resume_health import ResumeHealth
from kraken.resume_matcher import ResumeMatcher
from kraken.resume_profile import ResumeProfile


class Dashboard:
    """Generate a personalized dashboard."""

    def __init__(self) -> None:
        self.health = ResumeHealth()
        self.matcher = ResumeMatcher()
        self.learning = LearningRecommender()

    def build(
        self,
        profile: ResumeProfile,
        opportunities: list[Opportunity],
    ) -> dict:
        """Build a dashboard from a profile and opportunities."""

        resume_score = self.health.score(profile.resume_text)

        matches = []
        excellent_matches = 0
        total_match_score = 0
        learning_recommendations: set[str] = set()

        for opportunity in opportunities:
            match_score = self.matcher.match(
                profile.resume_text,
                opportunity,
            )

            matches.append(
                {
                    "title": opportunity.title,
                    "organization": opportunity.organization,
                    "match": match_score,
                }
            )

            total_match_score += match_score

            if match_score >= 90:
                excellent_matches += 1

                learning_recommendations.update(
                    self.learning.recommend(
                        profile,
                        opportunity,
                    )
                )

        matches.sort(
            key=lambda item: item["match"],
            reverse=True,
        )

        average_match = (
            round(total_match_score / len(opportunities))
            if opportunities
            else 0
        )

        return {
            "resume_health": resume_score,
            "total_jobs": len(opportunities),
            "excellent_matches": excellent_matches,
            "average_match": average_match,
            "learning_recommendations": sorted(
                learning_recommendations
            ),
            "top_matches": matches[:5],
        }
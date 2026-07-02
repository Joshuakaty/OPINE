"""Learning recommendation engine for OPINE."""

from __future__ import annotations

from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile
from kraken.skill_gap import SkillGapAnalyzer


class LearningRecommender:
    """Recommend what the user should learn next."""

    def __init__(self) -> None:
        self.analyzer = SkillGapAnalyzer()

    def recommend(
        self,
        profile: UserProfile,
        opportunity: Opportunity,
    ) -> list[str]:
        """Return prioritized learning recommendations."""

        missing = self.analyzer.missing_skills(
            profile,
            opportunity,
        )

        return sorted(missing)
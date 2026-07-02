"""Skill gap analysis for OPINE."""

from __future__ import annotations

from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile
from kraken.skills import SkillExtractor


class SkillGapAnalyzer:
    """Analyze missing skills for a user."""

    def __init__(self) -> None:
        self.extractor = SkillExtractor()

    def missing_skills(
        self,
        profile: UserProfile,
        opportunity: Opportunity,
    ) -> list[str]:
        """Return skills required by the opportunity but missing from the user."""

        required = self.extractor.extract(opportunity)

        user_skills = {
            skill.lower()
            for skill in profile.skills
        }

        return [
            skill
            for skill in required
            if skill.lower() not in user_skills
        ]
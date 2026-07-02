"""User opportunity matching."""

from __future__ import annotations

from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile


class OpportunityMatcher:
    """Match opportunities to a user profile."""

    def match(
        self,
        profile: UserProfile,
        opportunity: Opportunity,
    ) -> int:
        """Return a personal match score between 0 and 100."""

        score = 0

        text = (
            opportunity.title
            + " "
            + opportunity.description
        ).lower()

        # Skill matches
        for skill in profile.skills:
            if skill.lower() in text:
                score += 15

        # Desired role matches
        for role in profile.desired_roles:
            if role.lower() in opportunity.title.lower():
                score += 20

        # Preferred locations
        for location in profile.preferred_locations:
            if location.lower() in opportunity.location.lower():
                score += 15

        # Remote preference
        if profile.remote_only:
            if "remote" in opportunity.location.lower():
                score += 20
        else:
            score += 10

        return min(score, 100)
"""Explain why an opportunity matches a user."""

from __future__ import annotations

from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile


class MatchExplainer:
    """Generate human-readable match explanations."""

    def explain(
        self,
        profile: UserProfile,
        opportunity: Opportunity,
    ) -> list[str]:
        """Return a list of reasons why the opportunity matches."""

        reasons: list[str] = []

        text = (
            opportunity.title
            + " "
            + opportunity.description
        ).lower()

        for skill in profile.skills:
            if skill.lower() in text:
                reasons.append(f"Matches your {skill} skill")

        for role in profile.desired_roles:
            if role.lower() in opportunity.title.lower():
                reasons.append("Matches your preferred role")

        if profile.remote_only and "remote" in opportunity.location.lower():
            reasons.append("Matches your remote preference")

        if (
            profile.preferred_locations
            and opportunity.location in profile.preferred_locations
        ):
            reasons.append("Matches your preferred location")

        if opportunity.salary:
            reasons.append("Salary information available")

        if not reasons:
            reasons.append("General opportunity match")

        return reasons
"""Skill extraction utilities for OPINE."""

from __future__ import annotations

from kraken.opportunity import Opportunity


class SkillExtractor:
    """Extract known skills from an opportunity."""

    KNOWN_SKILLS = {
        "python",
        "fastapi",
        "django",
        "flask",
        "docker",
        "kubernetes",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "aws",
        "azure",
        "gcp",
        "git",
        "linux",
        "javascript",
        "typescript",
        "react",
        "vue",
    }

    def extract(self, opportunity: Opportunity) -> list[str]:
        """Return a sorted list of detected skills."""

        text = (
            opportunity.title
            + " "
            + opportunity.description
        ).lower()

        found = [
            skill
            for skill in self.KNOWN_SKILLS
            if skill in text
        ]

        return sorted(found)
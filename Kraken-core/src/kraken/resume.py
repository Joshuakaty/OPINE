"""Resume analysis utilities for OPINE."""

from __future__ import annotations

from kraken.skills import SkillExtractor


class ResumeAnalyzer:
    """Extract skills from resume text."""

    def __init__(self) -> None:
        self.known_skills = SkillExtractor.KNOWN_SKILLS

    def extract_skills(self, resume_text: str) -> list[str]:
        """Return skills detected in the resume."""

        text = resume_text.lower()

        skills = [
            skill
            for skill in self.known_skills
            if skill in text
        ]

        return sorted(skills)
"""Resume matching engine for OPINE."""

from __future__ import annotations

from kraken.opportunity import Opportunity
from kraken.resume import ResumeAnalyzer
from kraken.skills import SkillExtractor


class ResumeMatcher:
    """Match a resume against opportunities."""

    def __init__(self) -> None:
        self.resume = ResumeAnalyzer()
        self.skills = SkillExtractor()

    def match(
        self,
        resume_text: str,
        opportunity: Opportunity,
    ) -> int:
        """Return a resume match score between 0 and 100."""

        resume_skills = set(
            self.resume.extract_skills(resume_text)
        )

        job_skills = set(
            self.skills.extract(opportunity)
        )

        if not job_skills:
            return 0

        matches = len(resume_skills & job_skills)

        return round(matches / len(job_skills) * 100)
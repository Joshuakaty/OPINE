"""Resume health scoring for OPINE."""

from __future__ import annotations

from kraken.resume import ResumeAnalyzer


class ResumeHealth:
    """Calculate a resume health score."""

    MAX_SCORE = 100
    MAX_SKILLS = 10

    def __init__(self) -> None:
        self.analyzer = ResumeAnalyzer()

    def score(self, resume_text: str) -> int:
        """Return a score between 0 and 100."""

        skills = self.analyzer.extract_skills(resume_text)

        return round(
            min(len(skills), self.MAX_SKILLS)
            / self.MAX_SKILLS
            * self.MAX_SCORE
        )
"""Resume profile for OPINE."""

from __future__ import annotations

from dataclasses import dataclass, field

from kraken.resume import ResumeAnalyzer


@dataclass
class ResumeProfile:
    """Stores a user's resume and extracted skills."""

    resume_text: str = ""
    skills: list[str] = field(default_factory=list)

    def update(self, resume_text: str) -> None:
        """Update the stored resume and extracted skills."""

        analyzer = ResumeAnalyzer()

        self.resume_text = resume_text
        self.skills = analyzer.extract_skills(resume_text)
"""User model for OPINE."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from kraken.resume_profile import ResumeProfile


@dataclass
class User:
    """Represents an OPINE user."""

    id: str
    name: str
    email: str

    resume_profile: ResumeProfile = field(
        default_factory=ResumeProfile
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    def update_resume(self, resume: str) -> None:
        """Update the user's resume."""

        self.resume_profile.update(resume)
        self.updated_at = datetime.utcnow()
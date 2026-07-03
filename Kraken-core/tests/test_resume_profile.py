"""Tests for resume profiles."""

from kraken.resume_profile import ResumeProfile


def test_resume_profile_update() -> None:
    """Updating a profile should extract skills."""

    profile = ResumeProfile()

    profile.update(
        """
        Python
        FastAPI
        Docker
        PostgreSQL
        AWS
        """
    )

    assert "python" in profile.skills
    assert "fastapi" in profile.skills
    assert "docker" in profile.skills
    assert "postgresql" in profile.skills
    assert "aws" in profile.skills


def test_empty_resume_profile() -> None:
    """Empty resumes should clear extracted skills."""

    profile = ResumeProfile()

    profile.update("")

    assert profile.skills == []
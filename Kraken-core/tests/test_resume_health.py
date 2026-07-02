"""Tests for resume health."""

from kraken.resume_health import ResumeHealth


def test_resume_health_score() -> None:
    """A resume with several known skills should score correctly."""

    resume = """
    Python
    FastAPI
    Docker
    PostgreSQL
    AWS
    Git
    """

    health = ResumeHealth()

    assert health.score(resume) == 60


def test_empty_resume() -> None:
    """An empty resume should score zero."""

    health = ResumeHealth()

    assert health.score("") == 0
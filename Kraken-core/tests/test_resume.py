"""Tests for the resume analyzer."""

from kraken.resume import ResumeAnalyzer


def test_extract_resume_skills() -> None:
    """Skills should be extracted from resume text."""

    resume = """
    Python
    FastAPI
    Docker
    PostgreSQL
    AWS
    Git
    """

    analyzer = ResumeAnalyzer()

    skills = analyzer.extract_skills(resume)

    assert "python" in skills
    assert "fastapi" in skills
    assert "docker" in skills
    assert "postgresql" in skills
    assert "aws" in skills
    assert "git" in skills


def test_empty_resume() -> None:
    """An empty resume should return no skills."""

    analyzer = ResumeAnalyzer()

    assert analyzer.extract_skills("") == []
"""Tests for the Opportunity Intelligence Engine."""

from kraken.intelligence import OpportunityIntelligence
from kraken.opportunity import Opportunity


def test_analyze_python_remote_ai_job() -> None:
    """The intelligence engine should identify important job characteristics."""

    engine = OpportunityIntelligence()

    opportunity = Opportunity(
        id="1",
        title="Senior Python Engineer",
        organization="OpenAI",
        location="Remote",
        salary="$180000",
        score=95,
        source="RemoteOK",
        url="https://example.com/job/1",
        description="Python backend engineer building AI systems.",
    )

    insights = engine.analyze(opportunity)

    assert "Remote opportunity" in insights
    assert "Python role" in insights
    assert "Salary information available" in insights
    assert "AI company" in insights


def test_analyze_general_job() -> None:
    """Jobs without special characteristics should return a general insight."""

    engine = OpportunityIntelligence()

    opportunity = Opportunity(
        id="2",
        title="Office Administrator",
        organization="Example Ltd",
        location="Accra",
        salary="",
        score=20,
        source="RemoteOK",
        url="https://example.com/job/2",
        description="General office administration duties.",
    )

    insights = engine.analyze(opportunity)

    assert insights == ["General opportunity"]
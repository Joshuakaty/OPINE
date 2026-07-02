"""Tests for the match explainer."""

from kraken.match_explainer import MatchExplainer
from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile


def test_match_explanation() -> None:
    """A matching opportunity should produce useful explanations."""

    profile = UserProfile(
        name="Joshua",
        skills=["Python", "FastAPI"],
        desired_roles=["Backend Engineer"],
        preferred_locations=["Remote"],
        remote_only=True,
    )

    opportunity = Opportunity(
        id="1",
        title="Backend Engineer",
        organization="OpenAI",
        location="Remote",
        salary="$150000",
        score=95,
        source="RemoteOK",
        url="https://example.com/job",
        description="Python FastAPI backend development.",
    )

    explainer = MatchExplainer()

    reasons = explainer.explain(profile, opportunity)

    assert "Matches your Python skill" in reasons
    assert "Matches your FastAPI skill" in reasons
    assert "Matches your preferred role" in reasons
    assert "Matches your remote preference" in reasons
    assert "Salary information available" in reasons


def test_general_match() -> None:
    """Non-matching opportunities should return a general explanation."""

    profile = UserProfile(name="Joshua")

    opportunity = Opportunity(
        id="2",
        title="Office Administrator",
        organization="Example Ltd",
        location="Accra",
        salary="",
        score=20,
        source="RemoteOK",
        url="https://example.com/job2",
        description="General administration.",
    )

    explainer = MatchExplainer()

    reasons = explainer.explain(profile, opportunity)

    assert reasons == ["General opportunity match"]
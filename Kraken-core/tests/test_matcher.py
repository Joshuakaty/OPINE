"""Tests for the opportunity matcher."""

from kraken.matcher import OpportunityMatcher
from kraken.opportunity import Opportunity
from kraken.profile.user_profile import UserProfile


def test_match_python_remote_job() -> None:
    """A matching job should receive a high score."""

    profile = UserProfile(
        name="Joshua",
        skills=["Python", "FastAPI"],
        desired_roles=["Backend Engineer"],
        preferred_locations=["Remote"],
        remote_only=True,
        minimum_salary="$120000",
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

    matcher = OpportunityMatcher()

    match_score = matcher.match(profile, opportunity)

    assert match_score >= 70


def test_non_matching_job() -> None:
    """An unrelated job should receive a low score."""

    profile = UserProfile(
        name="Joshua",
        skills=["Python"],
        desired_roles=["Backend Engineer"],
        preferred_locations=["Remote"],
        remote_only=True,
    )

    opportunity = Opportunity(
        id="2",
        title="Marketing Manager",
        organization="Example Ltd",
        location="Accra",
        salary="",
        score=10,
        source="RemoteOK",
        url="https://example.com/job2",
        description="Marketing campaigns and sales strategy.",
    )

    matcher = OpportunityMatcher()

    match_score = matcher.match(profile, opportunity)

    assert match_score < 50
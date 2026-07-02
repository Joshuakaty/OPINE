"""Tests for the user profile model."""

from kraken.profile.user_profile import UserProfile


def test_create_user_profile() -> None:
    """A user profile should store user preferences."""

    profile = UserProfile(
        name="Joshua",
        skills=["Python", "FastAPI", "Docker"],
        desired_roles=["Backend Engineer"],
        preferred_locations=["Remote", "London"],
        remote_only=True,
        minimum_salary="$120000",
    )

    assert profile.name == "Joshua"
    assert "Python" in profile.skills
    assert "Backend Engineer" in profile.desired_roles
    assert "Remote" in profile.preferred_locations
    assert profile.remote_only is True
    assert profile.minimum_salary == "$120000"
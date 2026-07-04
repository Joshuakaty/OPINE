"""Tests for the user service."""

from kraken.users.service import UserService


def test_create_user() -> None:
    """Users should be created successfully."""

    service = UserService()

    user = service.create_user(
        user_id="1",
        name="Joshua",
        email="joshua@example.com",
    )

    assert user.id == "1"
    assert user.name == "Joshua"
    assert user.email == "joshua@example.com"

    assert service.total_users() == 1


def test_update_resume() -> None:
    """Updating a user's resume should populate the resume profile."""

    service = UserService()

    user = service.create_user(
        user_id="1",
        name="Joshua",
        email="joshua@example.com",
    )

    user.update_resume(
        """
        Python
        FastAPI
        Docker
        PostgreSQL
        """
    )

    assert "python" in user.resume_profile.skills
    assert "docker" in user.resume_profile.skills
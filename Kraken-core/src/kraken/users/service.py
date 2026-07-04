"""User service for OPINE."""

from __future__ import annotations

from kraken.users.user import User


class UserService:
    """Manage OPINE users."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def create_user(
        self,
        user_id: str,
        name: str,
        email: str,
    ) -> User:
        """Create a new user."""

        user = User(
            id=user_id,
            name=name,
            email=email,
        )

        self._users[user_id] = user

        return user

    def get_user(self, user_id: str) -> User | None:
        """Return a user by ID."""

        return self._users.get(user_id)

    def total_users(self) -> int:
        """Return the number of users."""

        return len(self._users)
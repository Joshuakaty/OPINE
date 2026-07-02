"""User profile model for OPINE."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class UserProfile:
    """Represents a user's job preferences."""

    name: str

    skills: list[str] = field(default_factory=list)

    desired_roles: list[str] = field(default_factory=list)

    preferred_locations: list[str] = field(default_factory=list)

    remote_only: bool = False

    minimum_salary: str = ""
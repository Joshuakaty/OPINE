"""Opportunity model."""

from dataclasses import dataclass


@dataclass(slots=True)
class Opportunity:
    """Represents a single opportunity."""

    id: str
    title: str
    source: str
    url: str
    location: str = ""
    organization: str = ""
    description: str = ""
    salary: str = ""
    score: int = 0
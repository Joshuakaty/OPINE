"""Deduplication utilities for OPINE."""

from __future__ import annotations

from kraken.opportunity import Opportunity


def deduplicate(
    opportunities: list[Opportunity],
) -> list[Opportunity]:
    """
    Remove duplicate opportunities.

    Duplicate opportunities are identified by their ID.
    """

    unique: dict[str, Opportunity] = {}

    for opportunity in opportunities:
        unique[opportunity.id] = opportunity

    return list(unique.values())
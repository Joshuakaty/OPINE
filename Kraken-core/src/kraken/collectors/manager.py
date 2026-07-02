"""Collector manager for OPINE."""

from __future__ import annotations

from kraken.opportunity import Opportunity


class CollectorManager:
    """Collect opportunities from multiple collectors."""

    def __init__(self) -> None:
        self.collectors = []

    def add_collector(self, collector) -> None:
        """Register a collector."""

        self.collectors.append(collector)

    def collect(self) -> list[Opportunity]:
        """Collect opportunities from all registered collectors."""

        opportunities: list[Opportunity] = []

        for collector in self.collectors:
            opportunities.extend(collector.collect())

        return opportunities
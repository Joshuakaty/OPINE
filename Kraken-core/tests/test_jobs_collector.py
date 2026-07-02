"""Tests for the JobsCollector."""

from kraken.collectors.jobs import JobsCollector


def test_collect_jobs() -> None:
    collector = JobsCollector()

    opportunities = collector.collect()

    assert len(opportunities) == 2
    assert opportunities[0].title == "Software Engineer"
    assert opportunities[1].organization == "Kraken Labs"
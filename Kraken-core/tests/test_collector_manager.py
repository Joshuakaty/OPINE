"""Tests for the collector manager."""

from kraken.collectors.manager import CollectorManager
from kraken.opportunity import Opportunity


class FakeCollector:
    """Simple fake collector for testing."""

    def collect(self):
        return [
            Opportunity(
                id="1",
                title="Python Developer",
                organization="OpenAI",
                location="Remote",
                salary="$120000",
                score=100,
                source="Fake",
                url="https://example.com/1",
                description="Backend Python",
            )
        ]


class AnotherFakeCollector:
    """Another fake collector for testing."""

    def collect(self):
        return [
            Opportunity(
                id="2",
                title="Backend Engineer",
                organization="Kraken Labs",
                location="Accra",
                salary="$90000",
                score=80,
                source="Fake",
                url="https://example.com/2",
                description="FastAPI",
            )
        ]


def test_collect_from_multiple_collectors() -> None:
    """CollectorManager should merge results from all collectors."""

    manager = CollectorManager()

    manager.add_collector(FakeCollector())
    manager.add_collector(AnotherFakeCollector())

    jobs = manager.collect()

    assert len(jobs) == 2
    assert jobs[0].id == "1"
    assert jobs[1].id == "2"
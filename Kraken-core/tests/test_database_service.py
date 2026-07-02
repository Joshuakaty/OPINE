"""Tests for the database service."""

from unittest.mock import patch

from kraken.opportunity import Opportunity
from kraken.services.database_service import DatabaseService


@patch("kraken.collectors.remoteok.RemoteOKCollector.collect")
def test_refresh_returns_ranked_jobs(mock_collect, tmp_path) -> None:
    """Refreshing should collect, score, save and return opportunities."""

    mock_collect.return_value = [
        Opportunity(
            id="1",
            title="Python Developer",
            organization="OpenAI",
            location="Remote",
            salary="$120000",
            score=0,
            source="RemoteOK",
            url="https://example.com/job/1",
            description="Backend Python",
        )
    ]

    service = DatabaseService(db_path=str(tmp_path / "test.db"))

    jobs = service.refresh()

    assert len(jobs) == 1
    assert jobs[0].title == "Python Developer"

    cached = service.get_cached()

    assert len(cached) == 1
    assert cached[0].id == "1"
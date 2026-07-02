"""Tests for the Arbeitnow collector."""

from unittest.mock import Mock, patch

from kraken.collectors.arbeitnow import ArbeitnowCollector


@patch("kraken.collectors.arbeitnow.httpx.get")
def test_collect_jobs(mock_get) -> None:
    """Collector should return opportunities from Arbeitnow."""

    mock_response = Mock()

    mock_response.json.return_value = {
        "data": [
            {
                "slug": "python-developer",
                "title": "Python Developer",
                "company_name": "OpenAI",
                "location": "Remote",
                "url": "https://example.com/job",
                "description": "Backend Python Developer",
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    collector = ArbeitnowCollector()

    jobs = collector.collect()

    assert len(jobs) == 1
    assert jobs[0].id == "python-developer"
    assert jobs[0].title == "Python Developer"
    assert jobs[0].organization == "OpenAI"
    assert jobs[0].source == "Arbeitnow"
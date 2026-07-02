"""Tests for loading opportunities from SQLite."""

from kraken.db.database import Database
from kraken.opportunity import Opportunity


def test_load_opportunities(tmp_path) -> None:
    """Loading opportunities should return saved records."""

    db_file = tmp_path / "test_opine.db"

    database = Database(str(db_file))
    database.initialize()

    opportunity = Opportunity(
        id="job-1",
        title="Python Developer",
        organization="OpenAI",
        location="Remote",
        salary="$100000",
        source="RemoteOK",
        url="https://example.com/job-1",
        description="Backend Python role",
    )

    database.save_opportunity(opportunity)

    opportunities = database.load_opportunities()

    assert len(opportunities) == 1
    assert opportunities[0].id == "job-1"
    assert opportunities[0].title == "Python Developer"
    assert opportunities[0].organization == "OpenAI"
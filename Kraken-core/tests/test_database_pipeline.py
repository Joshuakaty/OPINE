"""End-to-end database pipeline test."""

from kraken.db.database import Database
from kraken.opportunity import Opportunity


def test_database_pipeline(tmp_path) -> None:
    """Collected opportunities should be saved and loaded."""

    db_file = tmp_path / "pipeline.db"

    database = Database(str(db_file))
    database.initialize()

    opportunities = [
        Opportunity(
            id="1",
            title="Python Developer",
            organization="OpenAI",
            location="Remote",
            salary="$120000",
            score=100,
            source="RemoteOK",
            url="https://example.com/job/1",
            description="Backend Python",
        ),
        Opportunity(
            id="2",
            title="Backend Engineer",
            organization="Kraken Labs",
            location="Accra",
            salary="$90000",
            score=80,
            source="RemoteOK",
            url="https://example.com/job/2",
            description="FastAPI",
        ),
    ]

    for opportunity in opportunities:
        database.save_opportunity(opportunity)

    loaded = database.load_opportunities()

    assert len(loaded) == 2
    assert loaded[0].id == "1"
    assert loaded[1].id == "2"
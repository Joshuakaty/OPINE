"""Tests for saving opportunities to SQLite."""

import sqlite3

from kraken.db.database import Database
from kraken.opportunity import Opportunity


def test_save_opportunity(tmp_path) -> None:
    """Saving an opportunity should insert it into the database."""

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

    connection = sqlite3.connect(db_file)

    cursor = connection.execute(
        """
        SELECT id, title, organization
        FROM opportunities
        WHERE id = ?
        """,
        ("job-1",),
    )

    row = cursor.fetchone()

    connection.close()

    assert row is not None
    assert row[0] == "job-1"
    assert row[1] == "Python Developer"
    assert row[2] == "OpenAI"
"""Tests for the SQLite database."""

import sqlite3

from kraken.db.database import Database


def test_database_initialization(tmp_path) -> None:
    """Database should create the opportunities table."""

    db_file = tmp_path / "test_opine.db"

    database = Database(str(db_file))
    database.initialize()

    connection = sqlite3.connect(db_file)

    cursor = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='opportunities';"
    )

    table = cursor.fetchone()

    connection.close()

    assert table is not None
    assert table[0] == "opportunities"
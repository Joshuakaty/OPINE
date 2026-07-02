"""SQLite database manager for OPINE."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    """Manage the OPINE SQLite database."""

    def __init__(self, db_path: str = "opine.db") -> None:
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        """Return a SQLite connection."""
        return sqlite3.connect(self.db_path)

    def initialize(self) -> None:
        """Create the opportunities table if it does not exist."""

        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS opportunities (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    organization TEXT,
                    location TEXT,
                    salary TEXT,
                    score INTEGER,
                    source TEXT,
                    url TEXT,
                    description TEXT
                )
                """
            )
            connection.commit()

    def save_opportunity(self, opportunity) -> None:
        """Save an opportunity to the database."""

        with self.connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO opportunities (
                    id,
                    title,
                    organization,
                    location,
                    salary,
                    score,
                    source,
                    url,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    opportunity.id,
                    opportunity.title,
                    opportunity.organization,
                    opportunity.location,
                    opportunity.salary,
                    opportunity.score,
                    opportunity.source,
                    opportunity.url,
                    opportunity.description,
                ),
            )
            connection.commit()

    def load_opportunities(self) -> list:
        """Load all opportunities from the database."""

        from kraken.opportunity import Opportunity

        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    title,
                    organization,
                    location,
                    salary,
                    score,
                    source,
                    url,
                    description
                FROM opportunities
                """
            )

            rows = cursor.fetchall()

        return [
            Opportunity(
                id=row[0],
                title=row[1],
                organization=row[2],
                location=row[3],
                salary=row[4],
                score=row[5],
                source=row[6],
                url=row[7],
                description=row[8],
            )
            for row in rows
        ]
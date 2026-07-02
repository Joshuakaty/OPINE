"""Database service for OPINE."""

from __future__ import annotations

from kraken.collectors.remoteok import RemoteOKCollector
from kraken.db.database import Database
from kraken.opportunity import Opportunity
from kraken.ranking import OpportunityRanker
from kraken.scoring import OpportunityScorer


class DatabaseService:
    """Coordinates collecting, storing and serving opportunities."""

    def __init__(self, db_path: str = "opine.db") -> None:
        self.database = Database(db_path)
        self.collector = RemoteOKCollector()
        self.scorer = OpportunityScorer()
        self.ranker = OpportunityRanker()

        self.database.initialize()

    def refresh(self) -> list[Opportunity]:
        """
        Collect fresh opportunities, score them,
        save them to SQLite and return ranked results.
        """

        opportunities = self.collector.collect()

        for opportunity in opportunities:
            self.scorer.score(opportunity)
            self.database.save_opportunity(opportunity)

        return self.ranker.rank(opportunities)

    def get_cached(self) -> list[Opportunity]:
        """
        Return opportunities stored in SQLite.

        No internet connection is required.
        """

        opportunities = self.database.load_opportunities()

        return self.ranker.rank(opportunities)

    def refresh_and_cache(self) -> int:
        """
        Refresh the local database.

        Returns:
            Number of opportunities collected.
        """

        opportunities = self.collector.collect()

        for opportunity in opportunities:
            self.scorer.score(opportunity)
            self.database.save_opportunity(opportunity)

        return len(opportunities)
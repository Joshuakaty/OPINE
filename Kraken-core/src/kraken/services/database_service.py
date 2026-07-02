"""Database service for OPINE."""

from __future__ import annotations

from kraken.collectors.arbeitnow import ArbeitnowCollector
from kraken.collectors.manager import CollectorManager
from kraken.collectors.remoteok import RemoteOKCollector
from kraken.db.database import Database
from kraken.opportunity import Opportunity
from kraken.ranking import OpportunityRanker
from kraken.scoring import OpportunityScorer


class DatabaseService:
    """Coordinates collecting, storing and serving opportunities."""

    def __init__(self, db_path: str = "opine.db") -> None:
        self.database = Database(db_path)

        self.manager = CollectorManager()
        self.manager.add_collector(RemoteOKCollector())
        self.manager.add_collector(ArbeitnowCollector())

        self.scorer = OpportunityScorer()
        self.ranker = OpportunityRanker()

        self.database.initialize()

    def refresh(self) -> list[Opportunity]:
        """
        Collect fresh opportunities from all collectors,
        score them, save them and return ranked results.
        """

        opportunities = self.manager.collect()

        for opportunity in opportunities:
            self.scorer.score(opportunity)
            self.database.save_opportunity(opportunity)

        return self.ranker.rank(opportunities)

    def get_cached(self) -> list[Opportunity]:
        """
        Return opportunities stored in SQLite.
        """

        opportunities = self.database.load_opportunities()

        return self.ranker.rank(opportunities)

    def refresh_and_cache(self) -> int:
        """
        Refresh the local database from every collector.

        Returns:
            Number of opportunities collected.
        """

        opportunities = self.manager.collect()

        for opportunity in opportunities:
            self.scorer.score(opportunity)
            self.database.save_opportunity(opportunity)

        return len(opportunities)
"""Database service for OPINE."""

from __future__ import annotations

from kraken.collectors.remoteok import RemoteOKCollector
from kraken.db.database import Database
from kraken.opportunity import Opportunity
from kraken.ranking import OpportunityRanker
from kraken.scoring import OpportunityScorer


class DatabaseService:
    """Coordinates collecting, storing and loading opportunities."""

    def __init__(self, db_path: str = "opine.db") -> None:
        self.database = Database(db_path)
        self.collector = RemoteOKCollector()
        self.scorer = OpportunityScorer()
        self.ranker = OpportunityRanker()

        self.database.initialize()

    def refresh(self) -> list[Opportunity]:
        """Collect fresh opportunities and store them."""

        opportunities = self.collector.collect()

        for opportunity in opportunities:
            self.scorer.score(opportunity)
            self.database.save_opportunity(opportunity)

        return self.ranker.rank(opportunities)

    def get_cached(self) -> list[Opportunity]:
        """Return cached opportunities."""

        opportunities = self.database.load_opportunities()

        return self.ranker.rank(opportunities)
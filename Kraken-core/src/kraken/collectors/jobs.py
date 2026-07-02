"""Sample jobs collector."""

import json
from pathlib import Path

from kraken.opportunity import Opportunity


class JobsCollector:
    """Loads sample jobs from a local JSON file."""

    def collect(self) -> list[Opportunity]:
        data_file = Path("data/sample_jobs.json")

        with data_file.open("r", encoding="utf-8") as file:
            jobs = json.load(file)

        return [
            Opportunity(
                id=job["id"],
                title=job["title"],
                source=job["source"],
                url=job["url"],
                location=job["location"],
                organization=job["organization"],
                description=job["description"],
                salary=job["salary"],
            )
            for job in jobs
        ]
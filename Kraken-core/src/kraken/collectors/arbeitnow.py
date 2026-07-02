"""Arbeitnow collector for OPINE."""

from __future__ import annotations

import httpx

from kraken.opportunity import Opportunity


class ArbeitnowCollector:
    """Collect opportunities from the Arbeitnow API."""

    API_URL = "https://www.arbeitnow.com/api/job-board-api"

    def collect(self) -> list[Opportunity]:
        """Collect opportunities from Arbeitnow."""

        try:
            response = httpx.get(self.API_URL, timeout=30)
            response.raise_for_status()

            payload = response.json()

        except Exception as error:
            print(f"Arbeitnow request failed: {error}")
            return []

        opportunities: list[Opportunity] = []

        for job in payload.get("data", []):
            opportunities.append(
                Opportunity(
                    id=str(job.get("slug", "")),
                    title=job.get("title", ""),
                    organization=job.get("company_name", ""),
                    location=job.get("location", ""),
                    salary="",
                    score=0,
                    source="Arbeitnow",
                    url=job.get("url", ""),
                    description=job.get("description", ""),
                )
            )

        return opportunities
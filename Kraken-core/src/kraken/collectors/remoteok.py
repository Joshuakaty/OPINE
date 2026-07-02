"""RemoteOK job collector."""

from __future__ import annotations

from typing import Any

import httpx

from kraken.opportunity import Opportunity


class RemoteOKCollector:
    """Collect jobs from the RemoteOK API."""

    API_URL = "https://remoteok.com/api"

    def collect(self) -> list[Opportunity]:
        """Fetch jobs from RemoteOK."""

        headers = {
            "User-Agent": "OPINE/0.1 (+https://github.com/Joshuakaty/OPINE)",
            "Accept": "application/json",
        }

        try:
            response = httpx.get(
                self.API_URL,
                headers=headers,
                timeout=30.0,
                follow_redirects=True,
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:
            print(f"RemoteOK request failed: {exc}")
            return []

        data: list[dict[str, Any]] = response.json()

        opportunities: list[Opportunity] = []

        for job in data[1:]:
            opportunities.append(
                Opportunity(
                    id=str(job.get("id", "")),
                    title=job.get("position", ""),
                    source="RemoteOK",
                    url=job.get("url", ""),
                    location=job.get("location", "Remote"),
                    organization=job.get("company", ""),
                    description=job.get("description", ""),
                    salary=job.get("salary", ""),
                )
            )

        return opportunities
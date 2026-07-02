"""Collection commands."""

from rich.console import Console

from kraken.collectors.jobs import JobsCollector

console = Console()


def collect_jobs() -> None:
    """Collect sample jobs."""

    collector = JobsCollector()
    opportunities = collector.collect()

    console.print(f"[green]Collected {len(opportunities)} opportunities[/green]\n")

    for index, opportunity in enumerate(opportunities, start=1):
        console.print(f"{index}. {opportunity.title}")
        console.print(f"   Organization: {opportunity.organization}")
        console.print(f"   Location: {opportunity.location}\n")
"""Collection commands."""

from rich.console import Console

from kraken.collectors.jobs import JobsCollector
from kraken.ranking import OpportunityRanker
from kraken.scoring import OpportunityScorer

console = Console()


def collect_jobs() -> None:
    """Collect, score, rank and display jobs."""

    collector = JobsCollector()
    scorer = OpportunityScorer()
    ranker = OpportunityRanker()

    opportunities = collector.collect()

    for opportunity in opportunities:
        scorer.score(opportunity)

    opportunities = ranker.rank(opportunities)

    console.print(
        f"[green]Collected {len(opportunities)} opportunities[/green]\n"
    )

    for index, opportunity in enumerate(opportunities, start=1):
        console.print(
            f"[bold]{index}. {opportunity.title}[/bold] "
            f"[cyan](Score: {opportunity.score})[/cyan]"
        )
        console.print(f"   Organization: {opportunity.organization}")
        console.print(f"   Location: {opportunity.location}")
        console.print(f"   Salary: {opportunity.salary}\n")
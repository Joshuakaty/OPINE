"""Rich-rendered diagnostic report for the `kraken doctor` command.

This module is purely presentational: it renders diagnostic results it is
given to a `rich.console.Console`. It does not perform any checks itself —
see `kraken/diagnostics.py` for that logic.
"""

from rich.console import Console
from rich.table import Table

from ..diagnostics import CheckResult


def render_doctor_report(console: Console, results: list[CheckResult]) -> bool:
    """Render diagnostic check results as a Rich table.

    Args:
        console: The Rich `Console` instance to render output to.
        results: The diagnostic check results to display, in order.

    Returns:
        True if every check passed, otherwise False.
    """
    table = Table(title="KRAKEN Doctor", show_lines=False)
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Detail", style="dim")

    all_passed = True
    for result in results:
        if result.passed:
            status = "[bold green]PASS[/bold green]"
        else:
            status = "[bold red]FAIL[/bold red]"
            all_passed = False
        table.add_row(result.name, status, result.detail)

    console.print(table)
    return all_passed

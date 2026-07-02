"""Typer-based command-line interface for KRAKEN."""

import typer
from loguru import logger
from rich.console import Console

from .__version__ import __version__
from .config import get_settings
from .console.collect import collect_jobs
from .console.doctor import render_doctor_report
from .console.info import render_info_panel
from .console.welcome import render_welcome_screen
from .devtools import run_format, run_lint, run_tests
from .diagnostics import run_all_checks
from .info import gather_info
from .logging_config import configure_logging

app = typer.Typer(
    name="kraken",
    help="KRAKEN — internal engineering foundation for building OPINE.",
    add_completion=False,
    no_args_is_help=False,
)

console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Default command."""
    settings = get_settings()
    configure_logging(settings)
    logger.debug("KRAKEN CLI starting (invoked_subcommand={})", ctx.invoked_subcommand)

    if ctx.invoked_subcommand is None:
        render_welcome_screen(console, environment=settings.environment)


@app.command()
def version() -> None:
    """Show version."""
    console.print(f"KRAKEN v{__version__}")


@app.command()
def doctor() -> None:
    """Run diagnostics."""
    settings = get_settings()
    configure_logging(settings)

    results = run_all_checks(settings)
    all_passed = render_doctor_report(console, results)

    if not all_passed:
        raise typer.Exit(code=1)


@app.command()
def info() -> None:
    """Show configuration."""
    settings = get_settings()
    configure_logging(settings)

    snapshot = gather_info(settings)
    render_info_panel(console, snapshot)


@app.command(name="test")
def test_command() -> None:
    """Run tests."""
    settings = get_settings()
    configure_logging(settings)

    exit_code = run_tests()
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command(name="format")
def format_command(
    check: bool = typer.Option(False, "--check"),
) -> None:
    """Format code."""
    settings = get_settings()
    configure_logging(settings)

    exit_code = run_format(check=check)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command(name="lint")
def lint_command(
    fix: bool = typer.Option(False, "--fix"),
) -> None:
    """Lint code."""
    settings = get_settings()
    configure_logging(settings)

    exit_code = run_lint(fix=fix)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command("collect-jobs")
def collect_jobs_command() -> None:
    """Collect sample jobs."""
    collect_jobs()


if __name__ == "__main__":
    app()
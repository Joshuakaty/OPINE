"""Typer-based command-line interface for KRAKEN.

This module defines the CLI surface only. It does not perform any business
logic itself — it wires user input to the appropriate configuration,
logging, and presentation modules, following the composition-root pattern
described in ARCHITECTURE.md.
"""

import typer
from loguru import logger
from rich.console import Console

from .config import get_settings
from .console.doctor import render_doctor_report
from .console.info import render_info_panel
from .console.welcome import render_welcome_screen
from .devtools import run_format, run_lint, run_tests
from .diagnostics import run_all_checks
from .info import gather_info
from .logging_config import configure_logging
from .__version__ import __version__

# The Typer application instance exposed as the `kraken` console script.
app = typer.Typer(
    name="kraken",
    help="KRAKEN — internal engineering foundation for building OPINE.",
    add_completion=False,
    no_args_is_help=False,
)

# Shared Rich console instance used for all CLI output.
console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Run KRAKEN's default behavior when invoked with no subcommand.

    Loads and validates settings, configures logging, and — if no
    subcommand was requested — renders the welcome screen.

    Args:
        ctx: The Typer/Click context, used to detect whether a subcommand
            was invoked.
    """
    settings = get_settings()
    configure_logging(settings)
    logger.debug("KRAKEN CLI starting (invoked_subcommand={})", ctx.invoked_subcommand)

    if ctx.invoked_subcommand is None:
        render_welcome_screen(console, environment=settings.environment)


@app.command()
def version() -> None:
    """Print the installed KRAKEN version and exit.

    Prints the current KRAKEN package version to the console, using the
    single source of truth defined in `kraken/__version__.py`.
    """
    console.print(f"KRAKEN v{__version__}")


@app.command()
def doctor() -> None:
    """Run diagnostic checks against the current environment.

    Verifies the Python version, required dependencies, loaded
    configuration, and log directory writability, then prints a pass/fail
    report. Exits with a non-zero status code if any check fails, so it can
    be used as a CI gate.
    """
    settings = get_settings()
    configure_logging(settings)
    logger.debug("Running kraken doctor")

    results = run_all_checks(settings)
    all_passed = render_doctor_report(console, results)

    if not all_passed:
        raise typer.Exit(code=1)


@app.command()
def info() -> None:
    """Print a summary of KRAKEN's version, environment, and configuration.

    Useful for confirming what a running installation actually resolves to
    (version, active environment, log settings) without digging through
    environment variables by hand.
    """
    settings = get_settings()
    configure_logging(settings)
    logger.debug("Running kraken info")

    snapshot = gather_info(settings)
    render_info_panel(console, snapshot)


@app.command(name="test")
def test_command() -> None:
    """Run the project's test suite via pytest.

    Thin wrapper around `pytest`, so contributors don't need to remember
    the underlying tool or its invocation.
    """
    settings = get_settings()
    configure_logging(settings)
    logger.debug("Running kraken test")

    exit_code = run_tests()
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command(name="format")
def format_command(
    check: bool = typer.Option(
        False,
        "--check",
        help="Check formatting without modifying files.",
    ),
) -> None:
    """Format the codebase with Black.

    Thin wrapper around `black src tests`. Pass `--check` to verify
    formatting (e.g. in CI) without rewriting any files.
    """
    settings = get_settings()
    configure_logging(settings)
    logger.debug("Running kraken format (check={})", check)

    exit_code = run_format(check=check)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command(name="lint")
def lint_command(
    fix: bool = typer.Option(
        False,
        "--fix",
        help="Automatically fix fixable lint issues.",
    ),
) -> None:
    """Lint the codebase with Ruff.

    Thin wrapper around `ruff check src tests`. Pass `--fix` to
    automatically apply fixes for issues Ruff knows how to resolve.
    """
    settings = get_settings()
    configure_logging(settings)
    logger.debug("Running kraken lint (fix={})", fix)

    exit_code = run_lint(fix=fix)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


if __name__ == "__main__":
    app()

"""Application entry point (composition root) for KRAKEN.

This module is intentionally thin: its sole responsibility is to hand off
control to the CLI application. Any future alternative entry points
(e.g. a future API server) would live alongside this module, each acting
as its own composition root, without duplicating CLI-specific logic.
"""

from .cli import app


def run() -> None:
    """Run the KRAKEN application via its CLI entry point.

    This function is registered as the `kraken` console script in
    `pyproject.toml` and is also invoked when running this module
    directly with `python -m kraken.main`.
    """
    app()


if __name__ == "__main__":
    run()

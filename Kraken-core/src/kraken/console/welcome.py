"""Rich-rendered welcome screen for the KRAKEN CLI.

This module is purely presentational: it renders information it is given
to a `rich.console.Console`. It does not load configuration or perform any
logic beyond formatting output.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..constants import APP_NAME, APP_TAGLINE, TARGET_PRODUCT_NAME
from ..__version__ import __version__


def render_welcome_screen(console: Console, environment: str) -> None:
    """Render the KRAKEN welcome screen to the given console.

    Args:
        console: The Rich `Console` instance to render output to.
        environment: The active application environment (e.g. "local"),
            displayed to help engineers confirm their current context.
    """
    title = Text(f"{APP_NAME} v{__version__}", style="bold cyan")

    body = Text()
    body.append(f"{APP_TAGLINE}\n\n", style="white")
    body.append("Target product: ", style="dim")
    body.append(f"{TARGET_PRODUCT_NAME}\n", style="bold magenta")
    body.append("Environment:    ", style="dim")
    body.append(f"{environment}\n", style="bold yellow")
    body.append("Sprint:         ", style="dim")
    body.append("2 — Developer Productivity", style="bold green")

    panel = Panel(
        body,
        title=title,
        border_style="cyan",
        padding=(1, 4),
        expand=False,
    )

    console.print(panel)

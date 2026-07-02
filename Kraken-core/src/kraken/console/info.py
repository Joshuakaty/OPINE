"""Rich-rendered summary panel for the `kraken info` command.

This module is purely presentational: it renders the snapshot it is given
to a `rich.console.Console`. It does not gather any information itself —
see `kraken/info.py` for that logic.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..info import InfoSnapshot


def render_info_panel(console: Console, snapshot: InfoSnapshot) -> None:
    """Render an `InfoSnapshot` as a Rich panel.

    Args:
        console: The Rich `Console` instance to render output to.
        snapshot: The gathered runtime/configuration snapshot to display.
    """
    body = Text()
    body.append("Version:       ", style="dim")
    body.append(f"{snapshot.version}\n", style="bold cyan")
    body.append("Target product: ", style="dim")
    body.append(f"{snapshot.target_product}\n", style="bold magenta")
    body.append("CLI command:   ", style="dim")
    body.append(f"{snapshot.cli_command}\n", style="white")
    body.append("Python:        ", style="dim")
    body.append(f"{snapshot.python_version}\n", style="white")
    body.append("Platform:      ", style="dim")
    body.append(f"{snapshot.platform_description}\n", style="white")
    body.append("Environment:   ", style="dim")
    body.append(f"{snapshot.environment}\n", style="bold yellow")
    body.append("Log level:     ", style="dim")
    body.append(f"{snapshot.log_level}\n", style="white")
    body.append("Log to file:   ", style="dim")
    body.append(f"{snapshot.log_to_file}\n", style="white")
    body.append("Log directory: ", style="dim")
    body.append(f"{snapshot.log_dir}", style="white")

    panel = Panel(
        body,
        title=Text(f"{snapshot.app_name} — Info", style="bold cyan"),
        border_style="cyan",
        padding=(1, 4),
        expand=False,
    )

    console.print(panel)

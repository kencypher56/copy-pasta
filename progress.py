"""
progress.py – Real‑time progress bar with speed and ETA.
"""

import time
from rich.progress import (
    Progress, BarColumn, TextColumn, TimeRemainingColumn,
    TransferSpeedColumn, FileSizeColumn
)
from design import console, PROGRESS_STYLE

def create_progress_bar():
    """Create and return a rich Progress instance."""
    return Progress(
        TextColumn("[progress.description]{task.description}", style="rgb(255,215,0)"),
        BarColumn(bar_width=None, style="rgb(147,112,219)", complete_style="rgb(50,205,50)"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%", style="rgb(135,206,235)"),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        FileSizeColumn(),
        console=console,
        transient=True,
    )
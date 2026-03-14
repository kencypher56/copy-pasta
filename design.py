"""
design.py – CLI aesthetics, RGB colors, and animated Bugs Bunny.
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.color import Color
from rich.layout import Layout
from rich.live import Live

console = Console()

# RGB color styles
HEADER_STYLE   = Style(color=Color.from_rgb(255, 215, 0), bold=True)   # Gold
SUCCESS_STYLE  = Style(color=Color.from_rgb(50, 205, 50), bold=True)   # Lime green
ERROR_STYLE    = Style(color=Color.from_rgb(255, 69, 0), bold=True)    # Orange red
WARNING_STYLE  = Style(color=Color.from_rgb(255, 165, 0), bold=True)   # Orange
INFO_STYLE     = Style(color=Color.from_rgb(135, 206, 235), bold=True) # Sky blue
PROGRESS_STYLE = Style(color=Color.from_rgb(147, 112, 219))            # Medium purple

# ASCII art for Bugs Bunny
BUGS_ART = r"""
                 .--.
                /( @ >    ,-.
               / ' .'--._/  /
             :   ,    , .  /
             : (  '  'L  )  ;
             ( \  '.  )_\.'
              '. \^^^ ) ^^)
                )^) ^) ^) ^)
              /^ ^^ ^^ ^^ ^\
             {^  ^^  ^^  ^^  }
              \_____________/
"""

def bugs_bunny_animation(duration=3):
    """Play a smooth RGB-colored Bugs Bunny animation."""
    frames = [
        Panel(Text(BUGS_ART + "\n   \"What's up, doc?\"", style="bold rgb(255,215,0)"),
              border_style="rgb(255,215,0)", title="Bugs Bunny", title_align="left"),
        Panel(Text(BUGS_ART + "\n   \"What's up, doc?\"", style="bold rgb(255,255,0)"),
              border_style="rgb(255,255,0)", title="Bugs Bunny", title_align="left"),
        Panel(Text(BUGS_ART + "\n   \"What's up, doc?\"", style="bold rgb(255,105,180)"),
              border_style="rgb(255,105,180)", title="Bugs Bunny", title_align="left"),
    ]
    with Live(auto_refresh=False, console=console, screen=False) as live:
        end_time = time.time() + duration
        while time.time() < end_time:
            for frame in frames:
                live.update(frame)
                time.sleep(0.3)
        live.update(Panel("", border_style=""))

def show_banner():
    """Display the application banner."""
    console.rule("[bold rgb(255,215,0)]ADVANCED FILE TRANSFER UTILITY[/bold rgb(255,215,0)]")
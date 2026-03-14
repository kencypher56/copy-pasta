"""
sysinfo.py – Gather and display system information.
"""

import platform
import psutil
import subprocess
from rich.table import Table
from rich.panel import Panel
from design import console, INFO_STYLE

def get_gpu_info():
    """Return GPU information (cross-platform)."""
    system = platform.system()
    try:
        if system == "Windows":
            output = subprocess.check_output(
                "wmic path win32_VideoController get name", shell=True
            ).decode()
            lines = output.strip().split("\n")
            return lines[1].strip() if len(lines) > 1 else "N/A"
        elif system == "Linux":
            output = subprocess.check_output(
                "lspci | grep VGA", shell=True
            ).decode()
            return output.strip() or "N/A"
        elif system == "Darwin":  # macOS
            output = subprocess.check_output(
                "system_profiler SPDisplaysDataType | grep Chipset", shell=True
            ).decode()
            return output.strip() or "N/A"
    except:
        return "N/A"

def show_system_info():
    """Display CPU, RAM, Disk, GPU, OS in a rich table."""
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    gpu = get_gpu_info()

    table = Table(title="System Information", border_style="rgb(135,206,235)", box=None)
    table.add_column("Component", style="rgb(255,215,0)", no_wrap=True)
    table.add_column("Details", style="rgb(152,251,152)")

    table.add_row("OS", f"{platform.system()} {platform.release()} ({platform.version()})")
    table.add_row("CPU", f"{cpu_count} cores @ {cpu_freq.current:.2f} MHz (usage: {cpu_percent}%)")
    table.add_row("RAM", f"Total: {ram.total / (1024**3):.2f} GB, Available: {ram.available / (1024**3):.2f} GB ({ram.percent}% used)")
    table.add_row("Disk", f"Total: {disk.total / (1024**3):.2f} GB, Free: {disk.free / (1024**3):.2f} GB ({disk.percent}% used)")
    table.add_row("GPU", gpu)

    console.print(Panel(table, title="[bold rgb(50,205,50)]System Info[/bold rgb(50,205,50)]", title_align="left"))
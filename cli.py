"""
cli.py – Main command‑line interface integrating all modules.
"""

import sys
import os
import platform
import time
import threading
import questionary
from pathlib import Path

from design import console, bugs_bunny_animation, show_banner, SUCCESS_STYLE, ERROR_STYLE, WARNING_STYLE
from sysinfo import show_system_info
from cache import load_cache, save_cache, load_history, save_history, clear_cache
from progress import create_progress_bar
from copy import copy_file
from move import move_file
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.console import Group

# =============================================================================
#                          IMPROVED TRANSFER UI
# =============================================================================
class TransferUI:
    def __init__(self, total_files, total_size):
        self.total_files = total_files
        self.total_size = total_size
        self.processed_files = 0
        self.processed_size = 0
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.progress = create_progress_bar()
        self.task = self.progress.add_task("Transferring...", total=total_size)

    def update(self, added_size):
        with self.lock:
            self.processed_size += added_size
            self.processed_files += 1
            self.progress.update(self.task, completed=self.processed_size)

    def get_info_text(self):
        with self.lock:
            remaining = self.total_size - self.processed_size
            return (
                f"Files: {self.processed_files}/{self.total_files}  |  "
                f"Transferred: {self._format_size(self.processed_size)} / {self._format_size(self.total_size)}  |  "
                f"Remaining: {self._format_size(remaining)}"
            )

    def _format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def run(self, file_list, operation_func):
        """Run the transfer with live display."""
        def update_display(live):
            while not self.stop_event.is_set() or self.processed_files < self.total_files:
                time.sleep(0.2)
                # Group the progress bar and info text
                group = Group(
                    self.progress,
                    Text("\n"),
                    Text(self.get_info_text())
                )
                panel = Panel(
                    group,
                    border_style="rgb(147,112,219)",
                    title="[bold rgb(255,215,0)]Transfer in Progress[/bold rgb(255,215,0)]",
                    title_align="left",
                )
                live.update(panel)

        with Live(refresh_per_second=10, screen=False) as live:
            updater = threading.Thread(target=update_display, args=(live,))
            updater.daemon = True
            updater.start()

            failed = []
            for src, dst in file_list:
                try:
                    size = operation_func(src, dst)
                    self.update(size)
                except Exception as e:
                    failed.append((str(src), str(dst), str(e)))
                    with self.lock:
                        self.processed_files += 1  # count as processed even if failed

            self.stop_event.set()
            updater.join(timeout=1)

            if failed:
                console.print(f"\n[bold rgb(255,69,0)]Completed with {len(failed)} errors.[/bold rgb(255,69,0)]")
                for src, dst, err in failed[:5]:
                    console.print(f"  [rgb(255,182,193)]{src} → {dst}: {err}[/rgb(255,182,193)]")
                if len(failed) > 5:
                    console.print(f"  ... and {len(failed)-5} more")


# =============================================================================
#                          CONFLICT RESOLUTION
# =============================================================================
def conflict_resolver(conflicts):
    """Ask user what to do with conflicting files."""
    if not conflicts:
        return "replace", {}  # default
    console.print(f"[bold rgb(255,69,0)]Found {len(conflicts)} conflicting files.[/bold rgb(255,69,0)]")
    action = questionary.select(
        "How to handle conflicts?",
        choices=["Skip all", "Replace all", "Rename all"]
    ).ask()
    rename_map = {}
    if action == "Rename all":
        for src, dst in conflicts:
            base = dst.stem
            ext = dst.suffix
            counter = 1
            while True:
                new_name = f"{base} ({counter}){ext}"
                new_dst = dst.parent / new_name
                if not new_dst.exists():
                    rename_map[src] = new_dst
                    break
                counter += 1
    return action.lower(), rename_map


def collect_sources():
    """Let user add multiple source paths."""
    sources = []
    while True:
        choice = questionary.select(
            "Add source or finish?",
            choices=["Add file/directory", "Done"]
        ).ask()
        if choice == "Done":
            break
        path = questionary.path("Enter path (tab completion works):").ask()
        if path:
            p = Path(path).expanduser().resolve()
            if p.exists():
                sources.append(p)
                console.print(f"[rgb(50,205,50)]Added: {p}[/rgb(50,205,50)]")
            else:
                console.print("[rgb(255,69,0)]Path does not exist.[/rgb(255,69,0)]")
    return sources


# =============================================================================
#                                    MAIN
# =============================================================================
def main():
    bugs_bunny_animation()
    show_banner()
    os_name = platform.system()
    console.print(f"Detected OS: [rgb(50,205,50)]{os_name}[/rgb(50,205,50)]")

    while True:
        action = questionary.select(
            "Main Menu",
            choices=[
                "Copy file(s)",
                "Move file(s)",
                "Copy directory",
                "Move directory",
                "System Info",
                "View History",
                "Clear Cache",
                "Exit"
            ]
        ).ask()

        if action == "Exit":
            break
        elif action == "System Info":
            show_system_info()
        elif action == "View History":
            history = load_history()
            if history:
                for entry in history[-10:]:
                    console.print(entry)
            else:
                console.print("No history.")
        elif action == "Clear Cache":
            clear_cache()
            console.print("Cache cleared.", style=SUCCESS_STYLE)
        elif action.startswith("Copy") or action.startswith("Move"):
            # Common flow: select sources, destination, resolve conflicts, transfer
            console.print("[bold rgb(255,165,0)]Select source(s):[/bold rgb(255,165,0)]")
            sources = collect_sources()
            if not sources:
                continue

            dest = questionary.path("Destination directory:").ask()
            if not dest:
                continue
            dest_path = Path(dest).expanduser().resolve()
            if not dest_path.is_dir():
                console.print("Destination must be a directory.", style=ERROR_STYLE)
                continue

            # Determine if it's a directory operation
            is_dir_op = "directory" in action.lower()
            operation = "copy" if "Copy" in action else "move"

            # For directory ops, we expect one source; for file ops multiple allowed.
            if is_dir_op and len(sources) > 1:
                console.print("Directory operation supports only one source.", style=WARNING_STYLE)
                continue

            # Scan for conflicts and total size/files
            all_files = []   # list of (src, dst)
            conflicts = []
            total_size = 0
            total_files = 0

            for src in sources:
                if src.is_file():
                    dst = dest_path / src.name
                    all_files.append((src, dst))
                    total_files += 1
                    total_size += src.stat().st_size
                    if dst.exists():
                        conflicts.append((src, dst))
                else:
                    # directory
                    base_dst = dest_path / src.name
                    for root, dirs, files in os.walk(src):
                        rel = Path(root).relative_to(src)
                        dst_dir = base_dst / rel
                        for f in files:
                            src_file = Path(root) / f
                            dst_file = dst_dir / f
                            all_files.append((src_file, dst_file))
                            total_files += 1
                            total_size += src_file.stat().st_size
                            if dst_file.exists():
                                conflicts.append((src_file, dst_file))

            # Resolve conflicts
            conflict_action, rename_map = conflict_resolver(conflicts)

            # Filter/rename files according to conflict resolution
            final_files = []
            for src, dst in all_files:
                if dst.exists():
                    if conflict_action == "skip":
                        continue
                    elif conflict_action == "replace":
                        pass  # keep dst (will overwrite)
                    elif conflict_action == "rename":
                        if src in rename_map:
                            dst = rename_map[src]
                        else:
                            # fallback auto-rename
                            base = dst.stem
                            ext = dst.suffix
                            counter = 1
                            while True:
                                new_name = f"{base} ({counter}){ext}"
                                new_dst = dst.parent / new_name
                                if not new_dst.exists():
                                    dst = new_dst
                                    break
                                counter += 1
                final_files.append((src, dst))

            if not final_files:
                console.print("Nothing to transfer.", style=WARNING_STYLE)
                continue

            # Prepare the operation function
            if operation == "copy":
                op_func = lambda src, dst: copy_file(src, dst, verify=True)
            else:
                op_func = lambda src, dst: move_file(src, dst, verify=True)

            # Run transfer with improved UI
            ui = TransferUI(total_files, total_size)
            ui.run(final_files, op_func)

            # Log to history
            save_history({
                "action": action,
                "sources": [str(s) for s in sources],
                "destination": str(dest_path),
                "total_files": total_files,
                "timestamp": time.time()
            })

            console.print("All files transferred successfully!", style=SUCCESS_STYLE)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\nInterrupted by user.", style=WARNING_STYLE)
        sys.exit(0)
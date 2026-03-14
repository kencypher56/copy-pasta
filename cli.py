"""
cli.py – Main command‑line interface integrating all modules.
"""

import sys
import os
import platform
import time
import questionary
from pathlib import Path

from design import console, bugs_bunny_animation, show_banner, SUCCESS_STYLE, ERROR_STYLE, WARNING_STYLE
from sysinfo import show_system_info
from cache import load_cache, save_cache, load_history, save_history, clear_cache
from progress import create_progress_bar
from copy import copy_file
from move import move_file
from copydir import copy_directory
from movedir import move_directory

# For progress integration, we'll use a simple wrapper that updates a progress bar.
# In a real app, you'd integrate more tightly, but for brevity we'll show a progress bar
# for directory operations using rich progress and threading.

class TransferUI:
    def __init__(self, total_files, total_size):
        self.progress = create_progress_bar()
        self.task = self.progress.add_task("Transferring...", total=total_size)
        self.processed_size = 0
        self.processed_files = 0
        self.total_files = total_files

    def update(self, added_size):
        self.processed_size += added_size
        self.processed_files += 1
        self.progress.update(self.task, completed=self.processed_size)

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

            # For now, we assume single source for directory ops; for file ops we can handle multiple files.
            # We'll keep it simple: directory ops expect one source (directory), file ops can have multiple files.
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

            # Now perform the transfer with progress
            ui = TransferUI(total_files, total_size)
            failed = []

            # If it's a directory operation, we can use the specialized functions for efficiency.
            # But for simplicity, we'll just loop over files.
            with ui.progress:
                for src, dst in final_files:
                    try:
                        if operation == "copy":
                            size = copy_file(src, dst, verify=True)
                        else:
                            size = move_file(src, dst, verify=True)
                        ui.update(size)
                    except Exception as e:
                        failed.append((str(src), str(dst), str(e)))
                        ui.processed_files += 1  # count as processed even if failed

            # Log to history
            save_history({
                "action": action,
                "sources": [str(s) for s in sources],
                "destination": str(dest_path),
                "total_files": total_files,
                "failed": len(failed),
                "timestamp": time.time()
            })

            if failed:
                console.print(f"Completed with {len(failed)} errors.", style=ERROR_STYLE)
                for src, dst, err in failed[:5]:
                    console.print(f"  {src} -> {dst}: {err}")
            else:
                console.print("All files transferred successfully!", style=SUCCESS_STYLE)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\nInterrupted by user.", style=WARNING_STYLE)
        sys.exit(0)
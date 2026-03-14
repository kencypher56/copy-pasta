# copy-pasta

A modern, modular GUI file management tool with copy, move, and directory operations, progress tracking, system info, and automatic setup.

![Screenshot placeholder](screenshot.png)

## Features

- **Copy & Move** – Single files or entire directories.
- **Modern GUI** – Apple‑inspired light theme with Tailwind‑style icons.
- **Progress Tracking** – Real‑time progress bar and file count.
- **Conflict Resolution** – Skip, replace, or rename on the fly.
- **File Verification** – Optional SHA‑256 hash check.
- **System Info** – CPU, memory, disk usage displayed.
- **Recent Paths** – Caches recently used locations.
- **Automatic Setup** – Installs dependencies; falls back to virtual environment.

## Requirements

- Python 3.6 or higher
- Dependencies: `psutil`, `Pillow`, `sv-ttk` (installed automatically)

## Installation

1. Clone or download this repository.
2. Run the setup script:

   ```bash
   python setup.py
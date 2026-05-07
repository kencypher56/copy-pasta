<div align="center">

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                 ADVANCED FILE TRANSFER UTILITY (SINGLE FILE)              ║
║                    Copy/Move files & folders with style                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
              , ,
             /| |\
            / | | \
            | | | |     Neeaah, Whats up Doc !?!
            \ | | /
             \|w|/    /
             /_ _\   /      ,
  /\       _:()_():_       /]
  ||_     : ._=Y=_  :     / /
 [)(_\,   ',__\W/ _,'    /  \
 [) \_/\    _/'='\      /-/\)
  [_| \ \  ///  \ '._  / /
  :;   \ \///   / |  '` /
  ;::   \ `|:   : |',_.'
  """    \_|:   : |
           |:   : |'".
           /`._.'  \/
          /  /|   /
         |  \ /  /
          '. '. /
            '. '
            / \ \
           / / \'=,
     .----' /   \ (\__
snd (((____/     \ \  )
                  '.\_)
```

# 📁 Advanced File Transfer Utility

**A feature-rich, interactive CLI tool for copying and moving files with style.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/)
[![Rich](https://img.shields.io/badge/Rich-13.0%2B-ff69b4?style=for-the-badge)](https://github.com/Textualize/rich)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge&logo=github)](https://github.com/)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 **Copy & Move** | Handle single files or entire directories recursively |
| 📊 **Live Progress Bar** | Real-time percentage, speed, ETA, and file size |
| 🎨 **RGB Color Palette** | Elegant colors with an animated Bugs Bunny intro |
| ⚡ **Conflict Resolution** | Skip, replace, or auto-rename on file conflicts |
| 🖥️ **System Info** | Display CPU, RAM, disk, GPU, and OS at a glance |
| 🕓 **Operation History** | Cache of recent paths and the last 10 operations |
| 🔍 **Tab Completion** | Fully interactive menu with smart path completion |
| 🌐 **Cross-Platform** | Works on Linux, macOS, and Windows (including WSL) |
| 📦 **Single File** | Just download and run — no complex setup needed |

---

## 📦 Requirements

- **Python** `3.8` or newer
- The following packages:

| Package | Version |
|---|---|
| [`rich`](https://github.com/Textualize/rich) | `>= 13.0.0` |
| [`questionary`](https://github.com/tmbo/questionary) | `>= 2.0.0` |
| [`psutil`](https://github.com/giampaolo/psutil) | `>= 5.9.0` |

Install all dependencies in one command:

```bash
pip install rich questionary psutil
```

---

## 🚀 Quick Start

**1. Save the script**

```bash
# Save as fm.py (or any name you like)
curl -O https://raw.githubusercontent.com/your-username/your-repo/main/fm.py
```

**2. Install dependencies**

```bash
pip install rich questionary psutil
```

**3. Run the program**

```bash
python fm.py
```

> The interactive menu will appear immediately. Follow the on-screen prompts.

---

## 🎮 How to Use

When you launch the program, you'll be greeted with the main menu:

```
Main Menu:
  ▸ Copy file(s)
  ▸ Move file(s)
  ▸ Copy directory
  ▸ Move directory
  ▸ System Info
  ▸ View History
  ▸ Clear Cache
  ▸ Exit
```

### File & Directory Operations

- Enter source and destination paths using **tab completion** for speed.
- When a conflict is detected at the destination, choose how to handle it:

| Option | Behavior |
|---|---|
| ⏭️ **Skip all** | Keep existing files untouched |
| 🔄 **Replace all** | Overwrite all conflicting files |
| 🔢 **Rename all** | Auto-append a number (e.g., `file (1).txt`) |

### Live Progress Bar

During any transfer, the progress bar shows:

```
Copying... ████████████░░░░░░░░ 62% | 45.2 MB/s | ETA 00:03 | 280 MB / 450 MB
```

### Other Menu Options

- **System Info** — Hardware and OS details in a formatted table (CPU, RAM, GPU, Disk).
- **View History** — Last 10 operations: source, destination, timestamp, and status.
- **Clear Cache** — Wipe stored history and cached paths.

---

## 🛠️ Advanced Setup (Virtual Environment)

Running inside a virtual environment is optional but recommended for clean dependency management:

```bash
# Create and activate the environment
python -m venv .env
source .env/bin/activate        # Linux / macOS
# .env\Scripts\activate         # Windows

# Install dependencies
pip install rich questionary psutil

# Run
python fm.py
```

---

## 🔧 Troubleshooting

<details>
<summary><b>❌ ModuleNotFoundError: No module named 'rich' (or questionary / psutil)</b></summary>

Run the following and try again:

```bash
pip install rich questionary psutil
```

</details>

<details>
<summary><b>🔒 Permission errors when copying to system folders</b></summary>

- **Linux / macOS** — Prefix the command with `sudo`:
  ```bash
  sudo python fm.py
  ```
- **Windows** — Right-click your terminal and choose **Run as Administrator**.

</details>

<details>
<summary><b>🐢 Slow performance with many small files</b></summary>

The script uses multithreading via `ThreadPoolExecutor`. You can increase the worker count by editing the `workers` parameter in the source code to match your system's CPU core count.

</details>

<details>
<summary><b>🎨 Animation or colors don't look right</b></summary>

Ensure your terminal supports **true color (RGB)**. Recommended terminals:

| OS | Terminal |
|---|---|
| Windows | Windows Terminal |
| macOS | iTerm2 |
| Linux | GNOME Terminal, Kitty, Alacritty |

</details>

---

## 📄 License

This project is released under the [MIT License](LICENSE). You are free to use, modify, and distribute it as you wish.

---

<div align="center">

Made with ❤️ and a little help from Bugs Bunny 🐰

*"Neeaah, What's up Doc!?"*

</div>

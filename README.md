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
------------------------------------------------

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                              ✨ FEATURES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Copy or move single files or entire directories recursively.
• Real‑time progress bar with percentage, speed, ETA, and file size.
• Elegant RGB color palette and animated Bugs Bunny intro.
• Conflict resolution: skip, replace, or auto‑rename when files already exist.
• System information display (CPU, RAM, disk, GPU, OS).
• Caching of recent paths and operation history.
• Fully interactive menu with tab completion for paths.
• Cross‑platform: Linux, macOS, Windows (including WSL).
• Single‑file design – just download and run (after installing dependencies).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                          📦 REQUIREMENTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Python 3.8 or newer.
• The following Python packages:
    - rich >= 13.0.0
    - questionary >= 2.0.0
    - psutil >= 5.9.0

Install them with:

    pip install rich questionary psutil

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            🚀 QUICK START

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Save the script as `fm.py` (or any name you like).

2. Install dependencies (if not already present):

       pip install rich questionary psutil

3. Run the program:

       python fm.py

That's it! The interactive menu will appear. Follow the prompts to copy, move,
view system info, etc.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            🎮 HOW TO USE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When you start the program, you'll see the main menu:

    Main Menu:
      Copy file(s)
      Move file(s)
      Copy directory
      Move directory
      System Info
      View History
      Clear Cache
      Exit

• For file/directory operations, you will be asked to select source(s) and a
  destination. Use tab completion to quickly enter paths.

• If any files already exist at the destination, you can choose to:
    - Skip all (keep existing)
    - Replace all (overwrite)
    - Rename all (add a number, e.g., "file (1).txt")

• During transfer, a live progress bar shows:
    - Percentage complete
    - Transfer speed
    - Estimated time remaining
    - File size transferred / total

• "System Info" displays detailed hardware and OS information in a table.

• "View History" shows the last 10 operations (source, destination, timestamp,
  success/failure).

• "Clear Cache" removes the stored history and cached paths.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        🛠️ MANUAL SETUP (ADVANCED)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you prefer to run in a virtual environment (optional but recommended):

    python -m venv .env
    source .env/bin/activate        # Linux/macOS
    # .env\Scripts\activate         # Windows
    pip install rich questionary psutil
    python fm.py

The program does not include automatic venv handling – you are responsible
for installing the dependencies.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            🔧 TROUBLESHOOTING

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• "ModuleNotFoundError: No module named 'rich'" (or questionary/psutil)
    → Run `pip install rich questionary psutil` and try again.

• Permission errors when copying to system folders
    → On Linux/macOS, you may need to use `sudo`. On Windows, run as
      Administrator if necessary.

• Slow performance with many small files
    → The script uses multithreading for directory copies; you can adjust the
      number of workers by editing the `workers` parameter in the code (look
      for `ThreadPoolExecutor`).

• The animation or colors don't look right
    → Make sure your terminal supports true color (RGB). Most modern terminals
      (Windows Terminal, iTerm2, GNOME Terminal) do.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                          📄 LICENSE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This project is provided under the MIT License. Feel free to use, modify, and
distribute it as you wish.


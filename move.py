"""
move.py – Single file move operation (rename or copy+delete).
"""

import shutil
from pathlib import Path
from copy import copy_file

def move_file(src, dst, verify=True, buffer_size=1024*1024):
    """
    Move a file. If on same filesystem, use rename; else copy+delete.
    Returns bytes moved.
    """
    src = Path(src)
    dst = Path(dst)

    if src.parent.resolve() == dst.parent.resolve():
        # Same filesystem: rename
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        size = src.stat().st_size
        # rename doesn't verify; if needed, we could stat after move
        return size
    else:
        # Cross‑filesystem: copy then delete
        size = copy_file(src, dst, verify, buffer_size)
        src.unlink()
        return size
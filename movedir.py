"""
movedir.py – Recursive directory move (rename if same device, else copy+delete).
"""

import shutil
from pathlib import Path
from move import move_file
from copydir import copy_directory

def move_directory(src, dst, conflicts=None, verify=True, workers=None, buffer_size=1024*1024):
    """
    Move a directory recursively.
    Returns (total_files, total_bytes, failed_list).
    """
    src = Path(src)
    dst = Path(dst)

    # If same filesystem, we can just rename the whole directory
    if src.parent.resolve() == dst.parent.resolve():
        dst.parent.mkdir(parents=True, exist_ok=True)
        # Use shutil.move for atomic rename (works across devices but we limit)
        # Actually shutil.move uses os.rename if same device
        shutil.move(str(src), str(dst))
        # Count files after move? We could pre‑scan, but for simplicity return approximate
        total_files = sum(len(files) for _, _, files in os.walk(dst))
        total_bytes = sum(f.stat().st_size for f in dst.rglob('*') if f.is_file())
        return total_files, total_bytes, []
    else:
        # Cross‑filesystem: copy then delete
        files_copied, bytes_copied, failed = copy_directory(src, dst, conflicts, verify, workers, buffer_size)
        if not failed:
            shutil.rmtree(src)
        return files_copied, bytes_copied, failed
"""
copydir.py – Recursive directory copy with conflict handling.
"""

import shutil
from pathlib import Path
from copy import copy_file
from concurrent.futures import ThreadPoolExecutor, as_completed

def copy_directory(src, dst, conflicts=None, verify=True, workers=None, buffer_size=1024*1024):
    """
    Recursively copy a directory.
    conflicts: list of (src, dst) pairs that already exist.
    Returns (total_files, total_bytes, failed_list).
    """
    src = Path(src)
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)

    # Gather all files
    file_list = []
    for root, dirs, files in os.walk(src):
        rel_root = Path(root).relative_to(src)
        dst_dir = dst / rel_root
        dst_dir.mkdir(exist_ok=True)
        for f in files:
            src_file = Path(root) / f
            dst_file = dst_dir / f
            file_list.append((src_file, dst_file))

    # Conflict resolution could be applied here, but we'll handle in cli
    # For now, assume conflicts already resolved (dst may not exist)
    total_files = len(file_list)
    total_bytes = sum(f.stat().st_size for f, _ in file_list)
    failed = []
    copied_bytes = 0

    def copy_one(src_file, dst_file):
        nonlocal copied_bytes
        try:
            # If dst exists, caller should have resolved; we overwrite (or skip) based on flag
            # For simplicity, we just copy and overwrite
            size = copy_file(src_file, dst_file, verify, buffer_size)
            copied_bytes += size
            return True
        except Exception as e:
            failed.append((str(src_file), str(dst_file), str(e)))
            return False

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(copy_one, src_file, dst_file): (src_file, dst_file)
                   for src_file, dst_file in file_list}
        for future in as_completed(futures):
            future.result()  # raises if any exception

    return total_files, copied_bytes, failed
"""
copy.py – Single file copy operation with optional verification.
"""

import shutil
import hashlib
from pathlib import Path
from design import console, ERROR_STYLE, SUCCESS_STYLE

def hash_file(path, buffer_size=1024*1024):
    """Return SHA‑256 hash of file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b''):
            h.update(chunk)
    return h.hexdigest()

def copy_file(src, dst, verify=True, buffer_size=1024*1024):
    """
    Copy a single file from src to dst.
    Returns bytes copied.
    """
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)

    # Copy with progress? No, progress is handled at higher level.
    shutil.copy2(src, dst)  # copy2 preserves metadata

    if verify:
        src_hash = hash_file(src, buffer_size)
        dst_hash = hash_file(dst, buffer_size)
        if src_hash != dst_hash:
            raise ValueError(f"Hash mismatch: {src} -> {dst}")

    return src.stat().st_size
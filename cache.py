"""
cache.py – Simple JSON-based caching for file paths and history.
"""

import json
import os
from pathlib import Path

CACHE_DIR = Path.home() / ".file_manager"
CACHE_FILE = CACHE_DIR / "cache.json"
HISTORY_FILE = CACHE_DIR / "history.json"

def ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    CACHE_DIR.mkdir(exist_ok=True)

def load_cache():
    """Load cache from JSON file."""
    ensure_cache_dir()
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(data):
    """Save cache to JSON file."""
    ensure_cache_dir()
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_history():
    """Load operation history."""
    ensure_cache_dir()
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(entry):
    """Append an operation to history."""
    history = load_history()
    history.append(entry)
    # Keep last 100 entries
    if len(history) > 100:
        history = history[-100:]
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def clear_cache():
    """Delete cache files."""
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
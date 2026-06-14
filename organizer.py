"""
organizer.py
Core file-organization engine.
Scans a folder, categorizes every file, and moves it into the
appropriate sub-folder.  Reports progress via an optional callback
so the GUI can update in real time.
"""

import shutil
from pathlib import Path
from typing import Callable

from file_utils import (
    CATEGORY_MAP,
    get_category,
    resolve_destination,
    write_log,
)


# Result data-class (plain dict for simplicity)
def _empty_counts() -> dict[str, int]:
    """Return a zeroed-out count dict for every known category + Others."""
    counts = {cat: 0 for cat in CATEGORY_MAP}
    counts["Others"] = 0
    return counts


# Public API

def organize_folder(
    folder_path: str,
    progress_cb: Callable[[str], None] | None = None,
) -> dict:
    """
    Organize files inside *folder_path* into category sub-folders.

    Parameters:
   
    folder_path : str
        Absolute path of the folder to organize.
    progress_cb : callable, optional
        Receives a status string after each file is processed.
        Useful for updating a GUI label/log widget.

    Returns:

    dict with keys:
        total_scanned  – int
        total_moved    – int
        skipped        – int
        errors         – int
        category_counts – dict[str, int]
        log_entries    – list[str]
        log_path       – Path
    """
    folder = Path(folder_path).resolve()

    #  Validate 
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    #  Collect top-level files only (skip sub-dirs) 
    all_files = [p for p in folder.iterdir() if p.is_file()]

    total_scanned  = len(all_files)
    total_moved    = 0
    skipped        = 0
    errors         = 0
    category_counts = _empty_counts()
    log_entries: list[str] = []

    def _log(msg: str) -> None:
        log_entries.append(msg)
        if progress_cb:
            progress_cb(msg)

    _log(f"Folder   : {folder}")
    _log(f"Files found: {total_scanned}")
    _log("-" * 50)

    #  Process each file 
    for file_path in all_files:
        filename = file_path.name
        category = get_category(file_path)

        # Target sub-folder
        dest_dir = folder / category
        try:
            dest_dir.mkdir(exist_ok=True)
        except OSError as exc:
            _log(f"[ERROR]  Cannot create '{category}/' — {exc}")
            errors += 1
            continue

        # Resolve a safe (non-overwriting) destination path
        dest_path = resolve_destination(dest_dir, filename)
        renamed   = dest_path.name != filename  # True if a suffix was added

        try:
            shutil.move(str(file_path), str(dest_path))
            category_counts[category] += 1
            total_moved += 1

            note = f" (renamed → {dest_path.name})" if renamed else ""
            _log(f"[MOVED]  {filename}  →  {category}/{dest_path.name}{note}")

        except Exception as exc:  # noqa: BLE001
            _log(f"[ERROR]  {filename}  —  {exc}")
            errors += 1

    #  Summary 
    _log("-" * 50)
    _log(f"Total scanned : {total_scanned}")
    _log(f"Total moved   : {total_moved}")
    _log(f"Skipped       : {skipped}")
    _log(f"Errors        : {errors}")
    _log("")
    _log("Category breakdown:")
    for cat, count in category_counts.items():
        if count:
            _log(f"  {cat:<14}: {count}")

    #  Write log file 
    log_path = folder / "organization_log.txt"
    write_log(log_path, log_entries)

    return {
        "total_scanned":   total_scanned,
        "total_moved":     total_moved,
        "skipped":         skipped,
        "errors":          errors,
        "category_counts": category_counts,
        "log_entries":     log_entries,
        "log_path":        log_path,
    }

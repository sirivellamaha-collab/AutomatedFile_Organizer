"""
file_utils.py
Low-level helpers for the Automated File Organizer.
Handles extension mapping, safe destination path resolution,
and log-file writing.
"""

from pathlib import Path
from datetime import datetime

# Category mapping

CATEGORY_MAP: dict[str, list[str]] = {
    "JPG_Files": ["jpg"],
    "JPEG_Files": ["jpeg"],
    "PNG_Files": ["png"],
    "GIF_Files": ["gif"],
    "BMP_Files": ["bmp"],
    "WEBP_Files": ["webp"],

    "PDF_Files": ["pdf"],
    "TXT_Files": ["txt"],
    "DOC_Files": ["doc"],
    "DOCX_Files": ["docx"],

    "XLS_Files": ["xls"],
    "XLSX_Files": ["xlsx"],

    "PPT_Files": ["ppt"],
    "PPTX_Files": ["pptx"],

    "MP3_Files": ["mp3"],
    "WAV_Files": ["wav"],
    "AAC_Files": ["aac"],

    "MP4_Files": ["mp4"],
    "AVI_Files": ["avi"],
    "MKV_Files": ["mkv"],
    "MOV_Files": ["mov"],

    "ZIP_Files": ["zip"],
    "RAR_Files": ["rar"],
    "SEVENZ_Files": ["7z"],

    "PY_Files": ["py"],
    "JSON_Files": ["json"],
    "CSV_Files": ["csv"],
    "HTML_Files": ["html"],
    "CSS_Files": ["css"],
    "JS_Files": ["js"],
}
# Build a flat reverse-lookup: extension → category
_EXT_LOOKUP: dict[str, str] = {}
for _category, _exts in CATEGORY_MAP.items():
    for _ext in _exts:
        _EXT_LOOKUP[_ext] = _category


def get_category(file_path: Path) -> str:
    """Return the category name for a given file based on its extension."""
    ext = file_path.suffix.lstrip(".").lower()
    return _EXT_LOOKUP.get(ext, "Others")


def resolve_destination(dest_dir: Path, filename: str) -> Path:
    """
    Return a unique destination path that does NOT overwrite an existing file.

    If `filename` already exists in `dest_dir`, a counter suffix is appended:
        document.pdf → document_1.pdf → document_2.pdf …
    """
    dest = dest_dir / filename
    if not dest.exists():
        return dest

    stem   = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        dest = dest_dir / new_name
        if not dest.exists():
            return dest
        counter += 1


def write_log(log_path: Path, entries: list[str]) -> None:
    """
    Write (or append) log entries to *log_path*.

    Each call opens a new timestamped session block inside the file so
    multiple runs are preserved.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    header = (
        "\n" + "=" * 60 + "\n"
        f"  Organization Session — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        + "=" * 60 + "\n"
    )

    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(header)
        for entry in entries:
            fh.write(entry + "\n")
        fh.write("\n")

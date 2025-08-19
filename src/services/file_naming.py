import os
import re
from datetime import datetime
from typing import Iterable, Optional


INVALID_CHARS = r"[^A-Za-z0-9._ -]+"


def sanitize(text: str) -> str:
    """Return a filesystem-safe slug for file names and folder names."""
    if text is None:
        return "untitled"
    text = text.strip()
    text = re.sub(INVALID_CHARS, "_", text)
    text = re.sub(r"\s+", " ", text)             # collapse whitespace
    text = re.sub(r"_+", "_", text)              # collapse underscores
    text = text.strip(" ._-")
    return text or "untitled"


def unique_path(directory: str, filename: str) -> str:
    """Return a unique file path in directory based on filename (adds (1), (2), ... if needed)."""
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(directory, filename)
    if not os.path.exists(candidate):
        return candidate
    i = 1
    while True:
        candidate_name = f"{base} ({i}){ext}"
        candidate = os.path.join(directory, candidate_name)
        if not os.path.exists(candidate):
            return candidate
        i += 1


def generate_file_name(base_name: str, include_date: bool = True, index: Optional[int] = None, ext: Optional[str] = None) -> str:
    base = sanitize(base_name)
    parts = [base]
    if include_date:
        parts.append(datetime.now().strftime("%Y%m%d"))
    if index is not None:
        parts.append(f"{index:03d}")
    stem = "_".join(parts)
    if ext:
        if not ext.startswith("."):
            ext = "." + ext
        return f"{stem}{ext}"
    return stem


def rename_files_in_directory(directory: str, base_name: str, include_date: bool = True, files: Optional[Iterable[str]] = None) -> int:
    """Rename files in directory with pattern '<base>_<date>_<###><ext>' ensuring uniqueness.

    Returns count renamed.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Not a directory: {directory}")

    entries = sorted(files) if files else sorted(
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    )
    count = 0
    for i, filename in enumerate(entries, start=1):
        old_path = os.path.join(directory, filename)
        _, ext = os.path.splitext(filename)
        new_name = generate_file_name(base_name, include_date=include_date, index=i, ext=ext)
        new_path = unique_path(directory, new_name)
        if os.path.normcase(old_path) == os.path.normcase(new_path):
            continue
        os.rename(old_path, new_path)
        count += 1
    return count
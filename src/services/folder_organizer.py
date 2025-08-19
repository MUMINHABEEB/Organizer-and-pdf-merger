"""Simplified Folder Organizer that moves ALL files (no skipping) into a dated tree.

Features:
 - No lock / skip heuristics: every file under base (except the destination _organized tree itself) is processed.
 - Client name heuristic: from filename; else parent directory; else top-level relative folder; else base directory name.
 - Destination path scheme: standard (YYYY/MM/DD/Client/Type) or sample (YYYY/MON/DD-MM-YYYY/Client/Type).
 - Safe move with fallbacks (copy+remove, handling read-only); duplicate names resolved via unique_path.
"""

from __future__ import annotations

import os, re, shutil, stat
from datetime import datetime
from typing import Dict, Optional, Tuple, Any

from services.file_naming import sanitize, unique_path

MONTHS = {"jan":1,"january":1,"feb":2,"february":2,"mar":3,"march":3,"apr":4,"april":4,"may":5,"jun":6,"june":6,"jul":7,"july":7,"aug":8,"august":8,"sep":9,"sept":9,"september":9,"oct":10,"october":10,"nov":11,"november":11,"dec":12,"december":12}
TYPE_KEYWORDS = ("Ledger","SOA","Invoice","Statement","Report")

class FolderOrganizer:
    def __init__(self, base_directory: str, dry_run: bool = False, output_root: Optional[str] = None, scheme: str = "standard"):
        self.base_directory = base_directory
        self.dry_run = dry_run
        self.output_root = output_root or os.path.join(self.base_directory, "_organized")
        self.scheme = scheme
        self.logs: list[dict[str, Any]] = []
        self.error_messages: list[str] = []

    def run(self) -> Dict[str, Any]:
        files = list(self._iter_files())
        moved = copied_only = skipped = errors = 0
        for src in files:
            fname = os.path.basename(src)
            try:
                meta = self.extract_metadata(fname, src_full_path=src)
                dest_dir = self.destination_for(meta)
                os.makedirs(dest_dir, exist_ok=True)
                dest_name = self.build_destination_name(fname, meta)
                dest_path = unique_path(dest_dir, dest_name)
                if not self.dry_run:
                    status = self._move_file(src, dest_path)
                    if status == "moved":
                        moved += 1
                    elif status == "copied_only":
                        copied_only += 1
                    elif status == "skipped_locked":
                        skipped += 1
                        continue
                    else:
                        moved += 1
                else:
                    moved += 1
                self.logs.append({"file": fname, "to": dest_path, "meta": meta})
            except Exception as e:
                errors += 1
                self.logs.append({"file": fname, "error": str(e)})
                if len(self.error_messages) < 10:
                    self.error_messages.append(f"{fname}: {e}")
        return {"moved": moved, "copied_only": copied_only, "skipped": skipped, "errors": errors, "total": len(files), "dry_run": self.dry_run, "first_errors": self.error_messages, "skipped_all": False, "logs": self.logs}

    def _iter_files(self):
        base = os.path.normcase(os.path.abspath(self.base_directory))
        out_root = os.path.normcase(os.path.abspath(self.output_root))
        for dirpath, dirnames, filenames in os.walk(base):
            n_dir = os.path.normcase(dirpath)
            if n_dir.startswith(out_root):
                dirnames[:] = []
                continue
            for fn in filenames:
                if fn.lower() in ("desktop.ini","thumbs.db") or fn.startswith("~$"):
                    continue
                yield os.path.join(dirpath, fn)

    # --- Backwards compatibility (legacy API used by webview_bootstrap) ---
    def _iter_source_files(self):  # pragma: no cover
        yield from self._iter_files()

    def _should_skip(self, filename: str) -> bool:  # pragma: no cover
        return False

    def _move_file(self, src: str, dest: str) -> str:
        try:
            shutil.move(src, dest)
            return "moved"
        except Exception:
            try:
                shutil.copy2(src, dest)
            except PermissionError:
                return "skipped_locked"
            except Exception:
                raise
            try:
                os.remove(src)
                return "moved"
            except PermissionError:
                try:
                    os.chmod(src, stat.S_IWRITE)
                    os.remove(src)
                    return "moved"
                except Exception:
                    return "copied_only"
            except Exception:
                return "copied_only"

    def extract_metadata(self, filename: str, src_full_path: Optional[str] = None) -> Dict[str, Any]:
        name, ext = os.path.splitext(filename)
        ext_lower = ext.lower()
        client, ftype, date_val = self._from_filename(name)
        if date_val is None:
            date_val = self._from_content_date(filename, ext_lower, src_full_path=src_full_path)
        if date_val is None:
            path_for_time = src_full_path or os.path.join(self.base_directory, filename)
            date_val = datetime.fromtimestamp(os.path.getmtime(path_for_time))
        # Fallback client naming
        if not client and src_full_path:
            parent_dir = os.path.basename(os.path.dirname(src_full_path))
            if parent_dir and parent_dir.lower() not in ("_organized",):
                client = parent_dir
        if not client:
            rel = os.path.relpath(src_full_path or '', self.base_directory)
            top = rel.split(os.sep)[0] if rel and rel != '.' else ''
            if top and top.lower() not in ('_organized',):
                client = top
        if not client:
            client = os.path.basename(os.path.normpath(self.base_directory)) or 'Unknown'
        yyyy, mm, dd = date_val.year, date_val.month, date_val.day
        client = sanitize(client)
        ftype = sanitize(ftype or self._type_from_extension(ext_lower))
        return {"client": client, "type": ftype, "date": date_val, "year": yyyy, "month": mm, "day": dd, "ext": ext_lower, "filename": filename}

    def destination_for(self, meta: Dict[str, Any]) -> str:
        if self.scheme == 'sample':
            mon = meta['date'].strftime('%b').upper()
            day_stamp = f"{meta['day']:02d}-{meta['month']:02d}-{meta['year']:04d}"
            return os.path.join(self.output_root, f"{meta['year']:04d}", mon, day_stamp, meta['client'], meta['type'])
        return os.path.join(self.output_root, f"{meta['year']:04d}", f"{meta['month']:02d}", f"{meta['day']:02d}", meta['client'], meta['type'])

    def build_destination_name(self, original_filename: str, meta: Dict[str, Any]) -> str:
        _name, ext = os.path.splitext(original_filename)
        date_str = meta['date'].strftime('%Y%m%d')
        base = f"{meta['client']}_{meta['type']}_{date_str}"
        return f"{sanitize(base)}{ext}"

    def _type_from_extension(self, ext_lower: str) -> str:
        if ext_lower == '.eml': return 'Email'
        if ext_lower == '.rpt': return 'Report'
        if ext_lower in ('.pdf',): return 'PDF'
        return ext_lower.lstrip('.').upper()

    def _from_filename(self, name: str):
        client = None; ftype = None; date_val = None
        normalized = name.replace('_',' ')
        for t in TYPE_KEYWORDS:
            m = re.search(rf"\b{re.escape(t)}\b", normalized, re.IGNORECASE)
            if m:
                ftype = t.title()
                seg = normalized[:m.start()].strip()
                if seg: client = seg
                break
        m = re.search(r"\b(\d{2})-(\d{2})-(\d{4})\b", name)
        if m: date_val = _safe_date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        if date_val is None:
            m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", name)
            if m: date_val = _safe_date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if date_val is None:
            m = re.search(r"\b(\d{4})(\d{2})(\d{2})\b", name)
            if m: date_val = _safe_date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if date_val is None:
            m = re.search(r"\b(\d{1,2})[-_ ]?([A-Za-z]{3,9})[-_ ]?(\d{4})\b", name)
            if m:
                mon = MONTHS.get(m.group(2).lower()[:3])
                if mon: date_val = _safe_date(int(m.group(3)), mon, int(m.group(1)))
        if not client:
            guess = re.split(r"[\[\(\-]", normalized)[0].strip()
            if guess: client = guess
        return client, ftype, date_val

    def _from_content_date(self, filename: str, ext_lower: str, src_full_path: Optional[str] = None):
        full = src_full_path or os.path.join(self.base_directory, filename)
        if ext_lower == '.pdf':
            try:
                text = ''
                try:
                    from PyPDF2 import PdfReader as _PdfReader  # type: ignore
                    r = _PdfReader(full)
                    for page in r.pages[:2]:
                        text += (getattr(page,'extract_text',None) or getattr(page,'extractText',lambda:'') )()
                except Exception:
                    import PyPDF2  # type: ignore
                    with open(full,'rb') as fp:
                        r = PyPDF2.PdfFileReader(fp)
                        pages = getattr(r,'numPages',0)
                        for i in range(min(2,pages)):
                            page = r.getPage(i)
                            text += (getattr(page,'extractText',None) or getattr(page,'extract_text',lambda:'') )()
                return self._search_date_in_text(text)
            except Exception:
                return None
        if ext_lower == '.eml':
            try:
                import email; from email.utils import parsedate_to_datetime
                with open(full,'rb') as f: msg = email.message_from_bytes(f.read())
                if msg.get('Date'):
                    try: return parsedate_to_datetime(msg.get('Date'))
                    except Exception: pass
                subj = msg.get('Subject','')
                return self._search_date_in_text(subj) or None
            except Exception:
                return None
        return None

    def _search_date_in_text(self, text: str):
        m = re.search(r"\b(\d{2})[-/](\d{2})[-/](\d{4})\b", text)
        if m: return _safe_date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        m = re.search(r"\b(\d{4})[-/](\d{2})[-/](\d{2})\b", text)
        if m: return _safe_date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.search(r"\b(\d{1,2})[-\s]?([A-Za-z]{3,9})[-\s]?(\d{4})\b", text)
        if m:
            mon = MONTHS.get(m.group(2).lower()[:3])
            if mon: return _safe_date(int(m.group(3)), mon, int(m.group(1)))
        return None

def _safe_date(yyyy: int, mm: int, dd: int):
    try: return datetime(yyyy, mm, dd)
    except ValueError: return None
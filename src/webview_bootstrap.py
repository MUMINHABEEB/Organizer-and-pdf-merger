"""PyWebview bootstrap to provide a modern HTML UI inside the Windows .exe.

This does NOT expose a remote server – everything stays local.
"""
from __future__ import annotations

import json
import threading
import traceback
from pathlib import Path
import sys
import os
import subprocess
import time
import platform

# --- Optional service imports (safe) ---
try:
    from services.folder_organizer import FolderOrganizer
except Exception:
    FolderOrganizer = None
try:
    from PyPDF2 import PdfMerger
except Exception:
    PdfMerger = None

FRONTEND_DIR_NAME = "web"
ENTRY_FILE = "index.html"
APP_NAME = "AI_Automation_Suite"

DEFAULT_SETTINGS = {
    "last_folder": "",
    "preferred_scheme": "standard",
    "theme": "dark",
    "auto_open_merged": False,
    "version_seen": ""
}

def config_dir() -> Path:
    """Return platform-appropriate writable config directory."""
    # Windows
    if os.name == 'nt':
        base = os.environ.get('APPDATA') or str(Path.home() / 'AppData' / 'Roaming')
        return Path(base) / APP_NAME
    # macOS
    if sys.platform == 'darwin':
        return Path.home() / 'Library' / 'Application Support' / APP_NAME
    # Linux / other
    return Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / APP_NAME

def settings_path() -> Path:
    return config_dir() / 'settings.json'

def load_settings_file() -> dict:
    p = settings_path()
    try:
        if p.is_file():
            with p.open('r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return DEFAULT_SETTINGS.copy()
                merged = DEFAULT_SETTINGS.copy()
                merged.update({k: v for k, v in data.items() if k in DEFAULT_SETTINGS})
                return merged
    except Exception:
        pass
    return DEFAULT_SETTINGS.copy()

def save_settings_file(data: dict) -> bool:
    try:
        cfg = config_dir()
        cfg.mkdir(parents=True, exist_ok=True)
        valid = DEFAULT_SETTINGS.copy()
        # Keep only expected keys; ignore extras
        for k in DEFAULT_SETTINGS:
            if k in data:
                valid[k] = data[k]
        with settings_path().open('w', encoding='utf-8') as f:
            json.dump(valid, f, indent=2)
        return True
    except Exception as e:
        print(f"[webview] save_settings error: {e}")
        return False

def is_frozen():
    return hasattr(sys, "_MEIPASS")

def frontend_candidates():
    if is_frozen():
        base = Path(sys._MEIPASS)
        yield base / FRONTEND_DIR_NAME
        yield base / "_internal" / FRONTEND_DIR_NAME
    here = Path(__file__).resolve().parent
    yield here / FRONTEND_DIR_NAME
    yield here.parent / FRONTEND_DIR_NAME
    yield Path.cwd() / FRONTEND_DIR_NAME

def resolve_entry():
    searched = []
    for root in frontend_candidates():
        idx = root / ENTRY_FILE
        searched.append(str(idx))
        if idx.is_file():
            return idx, searched
    return None, searched

def fallback_html(error_msg, searched):
    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>UI Fallback</title>
<style>body{{background:#111;color:#eee;font-family:Segoe UI,Arial;padding:28px;}}
h1{{margin-top:0}} code{{background:#222;padding:2px 5px;border-radius:4px;}}
pre{{font-size:11px;white-space:pre-wrap;background:#161616;padding:8px;border-radius:6px;}}
</style></head><body>
<h1>Frontend Not Found</h1>
<p>{error_msg}</p>
<p>Searched paths:</p>
<pre>{chr(10).join(searched)}</pre>
<p>Place your built files in <code>src/web</code> (index.html + assets/).</p>
</body></html>"""

try:
    import tkinter as _tk
    from tkinter import filedialog as _fd
except Exception:
    _tk = None
    _fd = None

class Api:
    def __init__(self):
        self._window = None
        self._last = None
        self._cached_settings = None
    # Organizer progress / cancellation state (class-level defaults; single instance expected)
    _org_job = None
    _org_cancel = threading.Event()
    _org_progress = {"total":0,"done":0,"dry_run":True,"running":False}

    def _dialog_window(self):
        if not self._window:
            raise RuntimeError("Window not attached")
        return self._window

    def attach_window(self, w):
        self._window = w

    def ping(self):
        return {"ok": True, "time": time.time()}

    # --- Settings & Info ---
    def load_settings(self):
        if self._cached_settings is None:
            self._cached_settings = load_settings_file()
        return self._cached_settings

    def save_settings(self, settings: dict):
        if not isinstance(settings, dict):
            return {"error": "settings must be object"}
        merged = self.load_settings().copy()
        for k in DEFAULT_SETTINGS:
            if k in settings:
                merged[k] = settings[k]
        if save_settings_file(merged):
            self._cached_settings = merged
            return {"ok": True}
        return {"error": "failed to save"}

    def app_info(self):
        version = "0.0.0-dev"
        # Try to read VERSION file near project root
        try:
            root = Path(__file__).resolve().parent.parent
            vf = root / 'VERSION'
            if vf.is_file():
                version = vf.read_text(encoding='utf-8').strip() or version
        except Exception:
            pass
        backend = getattr(self._window, 'gui', None)
        try:
            backend = str(backend)
        except Exception:
            backend = None
        return {
            "version": version,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "backend_used": backend
        }

    # --- Utility: open path after operations ---
    def open_path(self, path):
        if not path:
            return {"error": "no path"}
        try:
            p = Path(path)
            if not p.exists():
                return {"error": "path not found"}
            if os.name == 'nt':  # Windows
                os.startfile(str(p))  # type: ignore[attr-defined]
            elif sys.platform == 'darwin':
                subprocess.call(['open', str(p)])
            else:
                subprocess.call(['xdg-open', str(p)])
            return {"ok": True}
        except Exception as e:
            return {"error": str(e)}

    def organize(self, path, dry_run=True, scheme="standard"):
        if FolderOrganizer is None:
            return {"error": "FolderOrganizer not available"}
        from datetime import datetime
        def _ser(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, dict):
                return {k: _ser(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [_ser(x) for x in obj]
            return obj
        if self._org_progress.get("running"):
            return {"error":"organizer already running"}
        self._org_cancel.clear()
        self._org_progress = {"total":0,"done":0,"dry_run":dry_run,"running":True}
        def job():
            try:
                from services.file_naming import unique_path  # local import to avoid circular at top
                org = FolderOrganizer(path, dry_run=dry_run, scheme=scheme)
                # Pre-scan to count
                files = list(org._iter_source_files())  # internal use for progress
                self._org_progress["total"] = len(files)
                moved = 0; copied_only=0; skipped=0; errors=0; logs=[]; error_messages=[]
                for idx, src_path in enumerate(files):
                    if self._org_cancel.is_set():
                        break
                    try:
                        fname = os.path.basename(src_path)
                        if org._should_skip(fname):
                            skipped += 1
                            logs.append({"file": fname, "skipped": True, "reason": "Matched skip pattern"})
                            continue
                        meta = org.extract_metadata(fname, src_full_path=src_path)
                        dest_dir = org.destination_for(meta)
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_name = org.build_destination_name(fname, meta)
                        dest_path = unique_path(dest_dir, dest_name)
                        # Skip if already organized (same filename present)
                        existing_same = os.path.join(dest_dir, dest_name)
                        if os.path.exists(existing_same):
                            skipped += 1
                            logs.append({"file": fname, "skipped": True, "reason": "Already organized"})
                            continue
                        if not dry_run:
                            status = org._move_file(src_path, dest_path)
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
                        logs.append({"file": fname, "to": dest_path, "meta": meta})
                    except Exception as e:
                        errors += 1
                        if len(error_messages) < 10:
                            error_messages.append(f"{src_path}: {e}")
                        logs.append({"file": os.path.basename(src_path), "error": str(e)})
                    finally:
                        self._org_progress["done"] = idx+1
                result = {"moved": moved, "copied_only": copied_only, "skipped": skipped, "errors": errors, "total": self._org_progress["total"], "dry_run": dry_run, "first_errors": error_messages, "skipped_all": False, "logs": logs, "canceled": self._org_cancel.is_set()}
                self._last = _ser(result)
            except Exception as e:
                self._last = {"error": str(e), "trace": traceback.format_exc()}
            finally:
                self._org_progress["running"] = False
        self._org_job = threading.Thread(target=job, daemon=True)
        self._org_job.start()
        return {"status": "started"}

    def organizer_progress(self):
        return self._org_progress.copy()

    def organizer_cancel(self):
        if self._org_progress.get("running"):
            self._org_cancel.set()
            return {"ok": True}
        return {"ok": False, "note": "not running"}

    def last_result(self):
        return getattr(self, "_last", None)

    def merge_pdfs(self, files, output_path=None):
        if not PdfMerger:
            return {"error": "PdfMerger not available"}
        if not files:
            return {"error": "No files"}
        if output_path is None:
            first = Path(files[0])
            output_path = str(first.with_name(first.stem + "_merged.pdf"))
        try:
            merger = PdfMerger()
            for f in files:
                if isinstance(f, (list, tuple)):
                    return {"error": "Invalid file entry (nested sequence)"}
                if isinstance(f, Path):
                    f = str(f)
                if not isinstance(f, str):
                    return {"error": f"Invalid file type: {type(f)}"}
                merger.append(f)
            merger.write(output_path)
            merger.close()
            return {"status": "ok", "output": output_path}
        except Exception as e:
            return {"error": str(e), "trace": traceback.format_exc()}

    def pick_pdfs(self):
        try:
            # Use no filter due to backend filter issues; user may select any files then we filter .pdf
            raw = []
            try:
                raw = self._dialog_window().create_file_dialog(
                    dialog_type='open', allow_multiple=True
                ) or []
                print(f"[webview] pick_pdfs raw(no-filter)={raw!r}")
            except Exception as we:
                print(f"[webview] pywebview dialog failed: {we}. Falling back to tkinter filedialog.")
            # Fallback if pywebview failed or returned empty
            if not raw:
                try:
                    import tkinter as _tk
                    from tkinter import filedialog as _fd
                    _root = _tk.Tk()
                    _root.withdraw()
                    _root.attributes('-topmost', True)
                    tk_files = _fd.askopenfilenames(
                        title='Select PDF files',
                        filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')]
                    )
                    _root.destroy()
                    if tk_files:
                        raw = list(tk_files)
                        print(f"[webview] tkinter selected {raw!r}")
                except Exception as tk_e:
                    print(f"[webview] tkinter fallback failed: {tk_e}")
            norm = []
            def add_item(it):
                if isinstance(it, (list, tuple)):
                    for sub in it:
                        add_item(sub)
                else:
                    if isinstance(it, Path):
                        it = str(it)
                    if isinstance(it, str):
                        if it.lower().endswith('.pdf'):
                            norm.append(it)
            add_item(raw)
            if not norm:
                return {"files": [], "note": "No PDF files selected (non-PDFs filtered)."}
            return {"files": norm}
        except Exception as e:
            return {"error": str(e)}

    def pick_save_pdf(self, default_name="merged.pdf"):
        try:
            try:
                target = self._dialog_window().create_file_dialog(
                    dialog_type='save', save_filename=default_name
                )
                print(f"[webview] pick_save_pdf raw(no-filter)={target!r}")
            except Exception as we:
                print(f"[webview] pywebview save dialog failed: {we}. Falling back to tkinter.")
                target = None
            if not target:
                # tkinter fallback
                try:
                    import tkinter as _tk
                    from tkinter import filedialog as _fd
                    _root = _tk.Tk()
                    _root.withdraw()
                    _root.attributes('-topmost', True)
                    tk_target = _fd.asksaveasfilename(
                        title='Save merged PDF as',
                        defaultextension='.pdf',
                        initialfile=default_name,
                        filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')]
                    )
                    _root.destroy()
                    if tk_target:
                        target = tk_target
                        print(f"[webview] tkinter save selected {target!r}")
                except Exception as tk_e:
                    print(f"[webview] tkinter save fallback failed: {tk_e}")
            if not target:
                return {"output": None}
            # pywebview returns a list for save in some backends
            if isinstance(target, (list, tuple)):
                target = target[0] if target else None
            return {"output": target}
        except Exception as e:
            return {"error": str(e)}

def main():
    try:
        print("[webview] bootstrap start")
        entry, searched = resolve_entry()
        print(f"[webview] frozen={is_frozen()} entry={entry}")
        html = None
        url = None
        if entry:
            url = str(entry)
        else:
            html = fallback_html("index.html not found", searched)

        print("[webview] importing webview module...")
        import webview
        print("[webview] webview imported successfully")
        
        api = Api()
        gui_order = ["edgechromium", "qt"]
        for backend in gui_order:
            try:
                print(f"[webview] trying backend={backend}")
                window = webview.create_window(
                    "AI Automation Suite (Web)",
                    url if url else None,
                    html=html,
                    js_api=api,
                    width=1180,
                    height=720,
                    min_size=(960, 600),
                )
                print(f"[webview] window created with backend={backend}")
                api.attach_window(window)
                print(f"[webview] starting webview with backend={backend}")
                webview.start(gui=backend, debug=True)
                return
            except Exception as e:
                print(f"[webview] backend {backend} failed: {e}")
                traceback.print_exc()

        # last resort generic
        print("[webview] all backends failed, generic fallback")
        import webview
        webview.create_window("AI Automation Suite (Fallback)", html=fallback_html("All backends failed", []))
        webview.start(debug=True)
        
    except Exception as e:
        print(f"[webview] FATAL ERROR in main(): {e}")
        traceback.print_exc()
        input("Press Enter to exit...")  # Keep console open to see error

if __name__ == "__main__":
    main()

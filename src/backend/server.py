"""FastAPI backend exposing organizer and PDF utilities for new web UI.
Run (dev): uvicorn backend.server:app --reload
"""
from __future__ import annotations

import os
import tempfile
import uuid
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from services.folder_organizer import FolderOrganizer
from PyPDF2 import PdfMerger

app = FastAPI(title="AI Automation Suite Backend", version="0.1.0")


class OrganizeRequest(BaseModel):
    base_directory: str
    dry_run: bool = True
    scheme: str = "standard"


@app.post("/organize")
def organize(req: OrganizeRequest):
    if not os.path.isdir(req.base_directory):
        return JSONResponse(status_code=400, content={"error": "base_directory not found"})
    org = FolderOrganizer(req.base_directory, dry_run=req.dry_run, scheme=req.scheme)
    result = org.run()
    # include truncated logs summary
    result["log_sample"] = org.logs[:25]
    return result


@app.post("/merge_pdfs")
async def merge_pdfs(files: List[UploadFile] = File(...), output_name: Optional[str] = Form(None)):
    if not files:
        return JSONResponse(status_code=400, content={"error": "No files uploaded"})
    tmpdir = tempfile.mkdtemp(prefix="merge_")
    merger = PdfMerger()
    paths: List[str] = []
    try:
        for f in files:
            data = await f.read()
            p = os.path.join(tmpdir, f.filename or f"file_{uuid.uuid4()}.pdf")
            with open(p, "wb") as out:
                out.write(data)
            merger.append(p)
            paths.append(p)
        out_name = output_name or (files[0].filename or "merged.pdf")
        if not out_name.lower().endswith('.pdf'):
            out_name += '.pdf'
        out_path = os.path.join(tmpdir, out_name)
        merger.write(out_path)
        merger.close()
        return FileResponse(out_path, filename=out_name, media_type="application/pdf")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        try:
            merger.close()
        except Exception:
            pass


@app.get("/health")
def health():
    return {"status": "ok"}

"""Tests for FastAPI backend endpoints.

Run all tests:
  pytest -q
"""
from __future__ import annotations

import io

import pytest
from fastapi.testclient import TestClient

from backend.server import app

client = TestClient(app)


def _make_sample_pdf(text: str = "Hello") -> bytes:
    """Create a minimal single-page PDF in memory containing the given text.
    Keeps it blank (PyPDF2 can't easily add text without extra deps, that's fine).
    """
    from PyPDF2 import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_organize_dry_run(tmp_path):
    f1 = tmp_path / "Al Hasoob Ledger (07-08-2025).pdf"
    f2 = tmp_path / "Capital Oldin Ledger (05-08-2025).pdf"
    f1.write_bytes(_make_sample_pdf())
    f2.write_bytes(_make_sample_pdf())

    payload = {
        "base_directory": str(tmp_path),
        "dry_run": True,
        "scheme": "standard",
    }
    r = client.post("/organize", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert data["moved"] == 2
    assert data["dry_run"] is True
    assert "log_sample" in data


def test_merge_pdfs():
    pdf1 = _make_sample_pdf("One")
    pdf2 = _make_sample_pdf("Two")

    files = [
        ("files", ("a.pdf", pdf1, "application/pdf")),
        ("files", ("b.pdf", pdf2, "application/pdf")),
    ]
    r = client.post("/merge_pdfs", files=files, data={"output_name": "merged_test.pdf"})
    assert r.status_code == 200
    assert r.content[:4] == b"%PDF"


def test_merge_pdfs_no_files():
    # FastAPI validation triggers 422 when required files field missing/empty
    r = client.post("/merge_pdfs", files=[])
    assert r.status_code == 422


def test_merge_pdfs_bad_pdf():
    # Upload a non-PDF payload with .pdf name to trigger merge exception path
    files = [
        ("files", ("bad.pdf", b"NOT_A_PDF", "application/pdf")),
    ]
    r = client.post("/merge_pdfs", files=files)
    # Depending on PyPDF2 behavior this may be 500 with error JSON
    assert r.status_code in (400, 500)
    if r.status_code == 500:
        assert "error" in r.json()


@pytest.mark.parametrize("invalid", ["/does/not/exist", "Z:/unlikely_path_12345"])
def test_organize_invalid_path(invalid):
    r = client.post("/organize", json={"base_directory": invalid, "dry_run": True})
    assert r.status_code == 400
    assert "error" in r.json()

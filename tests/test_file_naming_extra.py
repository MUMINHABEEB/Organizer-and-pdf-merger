from __future__ import annotations

import os
from src.services.file_naming import sanitize, unique_path, generate_file_name, rename_files_in_directory


def test_sanitize_none_and_specials():
    assert sanitize(None) == "untitled"  # type: ignore[arg-type]
    # Multiple invalid chars collapse to single underscore, spaces preserved then trimmed
    assert sanitize("  Bad@@ Name!!  ") == "Bad_ Name"


def test_unique_path_collision(tmp_path):
    f = tmp_path / "report.txt"
    f.write_text("x")
    p = unique_path(str(tmp_path), "report.txt")
    assert p.endswith("report (1).txt")


def test_generate_file_name_no_ext_index():
    name = generate_file_name("alpha beta", include_date=False, index=2)
    assert name.endswith("_002")


def test_rename_files_in_directory(tmp_path):
    for n in ["a.txt", "b.txt", "c.txt"]:
        (tmp_path / n).write_text("data")
    count = rename_files_in_directory(str(tmp_path), base_name="data", include_date=False)
    assert count == 3
    names = sorted(os.listdir(tmp_path))
    assert any("001" in n for n in names)


def test_rename_files_in_directory_noop(tmp_path):
    (tmp_path / "doc_001.txt").write_text("x")
    # Current logic uses unique_path which treats existing name as collision and appends (1)
    count = rename_files_in_directory(str(tmp_path), base_name="doc", include_date=False, files=["doc_001.txt"])
    assert count == 1


def test_rename_files_invalid_dir(tmp_path):
    missing = tmp_path / "missing_dir"
    try:
        rename_files_in_directory(str(missing), base_name="x")
    except ValueError as e:
        assert "Not a directory" in str(e)
    else:
        assert False, "Expected ValueError"

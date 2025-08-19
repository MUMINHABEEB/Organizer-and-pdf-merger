from src.services.file_naming import generate_file_name, sanitize

def test_generate_file_name_with_date_and_ext():
    name = generate_file_name("report", include_date=True, ext="txt")
    # Should start with report_ then 8 digit date then .txt
    assert name.startswith("report_")
    assert name.endswith(".txt")
    middle = name[len("report_"):-4]
    assert middle.isdigit() and len(middle) == 8

def test_generate_file_name_without_date():
    name = generate_file_name("report", include_date=False, ext="txt")
    assert name == "report.txt"

def test_generate_file_name_with_index():
    name = generate_file_name("invoice", include_date=True, index=5, ext="pdf")
    # invoice_YYYYMMDD_005.pdf
    assert name.startswith("invoice_") and name.endswith(".pdf")
    parts = name[:-4].split("_")
    assert len(parts) == 3
    assert parts[1].isdigit() and len(parts[1]) == 8
    assert parts[2] == "005"

def test_generate_file_name_empty_base():
    name = generate_file_name("", include_date=False, ext="txt")
    assert name == "untitled.txt"

def test_sanitize_removes_bad_chars():
    assert sanitize("Bad*Name?/") == "Bad_Name"
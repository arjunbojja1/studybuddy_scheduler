import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exporter.file_exporter import FileExporter

@pytest.fixture
def sample_schedule():
    return [
        {"course": "Math", "block": "study", "duration": 60, "date": "2023-11-10"},
        {"course": "Science", "block": "review", "duration": 30, "date": "2023-11-10"},
        {"course": "Math", "block": "study", "duration": 90, "date": "2023-11-11"}
    ]

def test_export_to_csv(sample_schedule):
    exporter = FileExporter()
    csv_output = exporter.export_to_csv(sample_schedule)

    # Check that CSV content includes headers and expected fields
    assert "course,block,duration,date" in csv_output
    assert "Math,study,60,2023-11-10" in csv_output
    assert csv_output.count("\n") >= 4  # Header + at least 3 rows

def test_export_to_txt(sample_schedule):
    exporter = FileExporter()
    txt_output = exporter.export_to_txt(sample_schedule)

    # Check formatting and content
    assert "2023-11-10 | Math | study | 60 min" in txt_output
    assert "2023-11-11 | Math | study | 90 min" in txt_output
    assert txt_output.count("\n") == 2  # 3 rows = 2 newlines
 
 
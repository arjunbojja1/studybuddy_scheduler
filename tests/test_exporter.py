"""Unit tests for the FileExporter.

This script tests the functionality of the FileExporter class, ensuring
that schedules are correctly exported to CSV and plain text formats.
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exporter.file_exporter import FileExporter

@pytest.fixture
def sample_schedule():
    """Provides a sample schedule for testing.

    Returns:
        list of dict: A list of schedule blocks with 'course', 'block',
        'duration', and 'date' keys.
    """
    return [
        {"course": "Math", "block": "study", "duration": 60, "date": "2023-11-10"},
        {"course": "Science", "block": "review", "duration": 30, "date": "2023-11-10"},
        {"course": "Math", "block": "study", "duration": 90, "date": "2023-11-11"}
    ]

def test_export_to_csv(sample_schedule):
    """Tests exporting the schedule to CSV format.

    Ensures that the CSV output includes headers and expected content.
    """
    exporter = FileExporter()
    csv_output = exporter.export_to_csv(sample_schedule)

    # Check that CSV content includes headers and expected fields
    assert "course,block,duration,date" in csv_output
    assert "Math,study,60,2023-11-10" in csv_output
    assert csv_output.count("\n") >= 4  # Header + at least 3 rows

def test_export_to_txt(sample_schedule):
    """Tests exporting the schedule to plain text format.

    Ensures that the text output is formatted correctly and includes expected content.
    """
    exporter = FileExporter()
    txt_output = exporter.export_to_txt(sample_schedule)

    # Check formatting and content
    assert "2023-11-10 | Math | study | 60 min" in txt_output
    assert "2023-11-11 | Math | study | 90 min" in txt_output
    assert txt_output.count("\n") == 2  # 3 rows = 2 newlines


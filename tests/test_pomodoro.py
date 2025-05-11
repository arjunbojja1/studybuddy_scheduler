import sys
import os
import pytest

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler.pomodoro import PomodoroScheduler

@pytest.fixture
def pomodoro_input():
    return [
        {"course": "History", "deadline": "2099-12-01", "hours": 3},
        {"course": "Biology", "deadline": "2099-11-25", "hours": 2},
    ]

def test_pomodoro_schedule_blocks(pomodoro_input):
    scheduler = PomodoroScheduler()
    schedule = scheduler.schedule(pomodoro_input)

    # Check that output is a non-empty list of blocks
    assert isinstance(schedule, list)
    assert len(schedule) > 0

    # Each block should contain expected keys
    for block in schedule:
        assert "course" in block
        assert "block" in block
        assert "duration" in block
        assert "date" in block

def test_pomodoro_block_lengths(pomodoro_input):
    scheduler = PomodoroScheduler()
    schedule = scheduler.schedule(pomodoro_input)

    for block in schedule:
        if block["block"] == "study":
            # Allow 25 or less
            assert 1 <= block["duration"] <= 25
        elif block["block"] == "break":
            # Allow short breaks
            assert block["duration"] in (5, 10)
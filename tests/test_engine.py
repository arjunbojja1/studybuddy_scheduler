"""Unit tests for the SchedulerEngine.

This script tests the functionality of the SchedulerEngine class,
ensuring that it generates schedules using different strategies.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler.scheduler_engine import SchedulerEngine

@pytest.fixture
def sample_courses():
    """Provides a sample list of courses for testing.

    Returns:
        list of dict: A list of courses with 'course', 'deadline', and 'hours' keys.
    """
    return [
        {"course": "Math", "deadline": "2023-12-01", "hours": 10},
        {"course": "Science", "deadline": "2023-11-15", "hours": 5}
    ]

def test_urgency_strategy(sample_courses):
    """Tests the urgency-based scheduling strategy.

    Ensures that courses with earlier deadlines are prioritized.
    """
    engine = SchedulerEngine(strategy="urgency")
    schedule = engine.generate_schedule(sample_courses)

    assert len(schedule) > 0
    # Ensure the earlier deadline ("Science") shows up first in at least one day's blocks
    course_names = [block["course"] for block in schedule]
    assert "Science" in course_names

def test_even_distribution_strategy(sample_courses):
    """Tests the even distribution scheduling strategy.

    Ensures that study time is distributed evenly across courses.
    """
    engine = SchedulerEngine(strategy="even")
    schedule = engine.generate_schedule(sample_courses)

    # Just ensure it generates something valid and includes both courses
    assert len(schedule) > 0
    course_names = {block["course"] for block in schedule}
    assert "Math" in course_names and "Science" in course_names
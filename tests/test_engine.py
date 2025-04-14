import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from scheduler.scheduler_engine import SchedulerEngine
from scheduler.strategy import UrgencyStrategy, EvenDistributionStrategy

class MockCourse:
    def __init__(self, name, deadline, estimated_time):
        self.name = name
        self.deadline = deadline
        self.estimated_time = estimated_time

class TestSchedulerEngine(unittest.TestCase):
    def setUp(self):
        self.courses = [
            MockCourse("Math", "2023-12-01", 10),
            MockCourse("Science", "2023-11-15", 5),
        ]

    def test_urgency_strategy(self):
        engine = SchedulerEngine(self.courses, UrgencyStrategy())
        schedule = engine.generate_schedule()
        self.assertEqual(schedule[0].name, "Science")

    def test_even_distribution_strategy(self):
        engine = SchedulerEngine(self.courses, EvenDistributionStrategy())
        schedule = engine.generate_schedule()
        self.assertEqual(len(schedule), 2)
        self.assertAlmostEqual(schedule[0]["allocated_time"], 66.67, places=2)
        self.assertAlmostEqual(schedule[1]["allocated_time"], 33.33, places=2)

if __name__ == "__main__":
    unittest.main()
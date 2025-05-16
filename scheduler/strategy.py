"""Scheduling strategies for the StudyBuddy Scheduler.

This script defines abstract and concrete scheduling strategies, including
urgency-based and even distribution strategies.
"""

from datetime import datetime, timedelta
from scheduler.utils import parse_date

class SchedulingStrategy:
    """Abstract base class for scheduling strategies."""

    def schedule(self, courses):
        """Schedules study blocks for the given courses.

        Args:
            courses (list of dict): List of courses, where each course is a
                dictionary containing 'course', 'deadline', and 'hours' keys.

        Returns:
            list of dict: A list of scheduled blocks.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError


class UrgencyStrategy(SchedulingStrategy):
    """Schedules study blocks based on course deadlines.

    Prioritizes courses with earlier deadlines.
    """

    def schedule(self, courses):
        """Generates a schedule based on urgency (earliest deadlines first).

        Args:
            courses (list of dict): List of courses, where each course is a
                dictionary containing 'course', 'deadline', and 'hours' keys.

        Returns:
            list of dict: A list of scheduled blocks, sorted by date.
        """
        today = datetime.today().date()
        schedule = []
        
        sorted_courses = sorted(courses, key=lambda c: parse_date(c['deadline']))
        
        for course in sorted_courses:
            try:
                total_minutes = int(float(course["hours"])) * 60
                deadline = parse_date(course["deadline"])
                days = (deadline - today).days + 1
                if days <= 0:
                    days = 1
            except (ValueError, KeyError):
                continue
            
            minutes_per_day = total_minutes // days
            extra_minutes = total_minutes % days
            
            for i in range(days):
                date = today + timedelta(days=i)
                duration = minutes_per_day + (1 if i < extra_minutes else 0)
                if duration > 0:
                    schedule.append({
                        "course": course["course"],
                        "block": "study",
                        "duration": duration,
                        "date": str(date)
                    })
        return schedule
            
class EvenDistributionStrategy(SchedulingStrategy):
    """Distributes study time evenly across the available days."""

    def schedule(self, courses):
        """Generates a schedule with evenly distributed study time.

        Args:
            courses (list of dict): List of courses, where each course is a
                dictionary containing 'course', 'deadline', and 'hours' keys.

        Returns:
            list of dict: A list of scheduled blocks, evenly distributed by date.
        """
        today = datetime.today().date()
        schedule = []     
        
        for course in courses:
            try:
                total_minutes = int(float(course["hours"])) * 60
                deadline = parse_date(course["deadline"])
                days = (deadline - today).days + 1
                if days <= 0:
                    days = 1
            except (ValueError, KeyError):
                continue
            
            minutes_per_day = total_minutes // days
            extra_minutes = total_minutes % days
            
            for i in range(days):
                date = today + timedelta(days=i)
                duration = minutes_per_day + (1 if i < extra_minutes else 0)
                if duration > 0:
                    schedule.append({
                        "course": course["course"],
                        "block": "study",
                        "duration": duration,
                        "date": str(date)
                    })
                    
        return schedule

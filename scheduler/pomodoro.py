"""Pomodoro scheduling for the StudyBuddy Scheduler.

This script defines the PomodoroScheduler class, which generates study
schedules using the Pomodoro technique.
"""

from datetime import datetime, timedelta
from scheduler.utils import parse_date

class PomodoroScheduler:
    """Schedules study sessions using the Pomodoro technique.

    Breaks study time into 25-minute study blocks followed by 5-minute breaks.
    """

    def schedule(self, courses):
        """Generates a Pomodoro-style schedule for the given courses.

        Args:
            courses (list of dict): List of courses, where each course is a
                dictionary containing 'course', 'deadline', and 'hours' keys.

        Returns:
            list of dict: A sorted list of schedule blocks, where each block
                contains 'course', 'block', 'duration', and 'date' keys.
        """
        schedule = []
        
        for course in sorted(courses, key=lambda c: parse_date(c['deadline'])):
            try:
                time_remaining = int(float(course["hours"])) * 60 # Convert hours to minutes
                deadline = parse_date(course["deadline"])
                
                start_date = datetime.today().date()
                
                date_range = [start_date + timedelta(days=i) for i in range((deadline - start_date).days + 1)]

                if (deadline - start_date).days < 0:
                    print(f"Skipping course '{course['course']}' — deadline has already passed.")
                    continue
                
                if not date_range:
                    continue
                
            except (ValueError, KeyError) as err:
                print(f"Error processing course {course['course']}: {err}")
                continue # Invalid input, skip this course
            
            date_index = 0
            blocks = []
            
            while time_remaining > 0:
                duration = min(25, time_remaining)
                assigned_date = date_range[date_index % len(date_range)]
                
                blocks.append({
                    "course": course["course"],
                    "block": "study",
                    "duration": duration,
                    "date": str(assigned_date)
                })
                
                time_remaining -= duration
                
                if time_remaining > 0:
                    blocks.append({
                        "course": course["course"],
                        "block": "break",
                        "duration": 5,
                        "date": str(assigned_date)
                    })
                date_index += 1
                
            schedule.extend(blocks)
                    
        return sorted(schedule, key=lambda x: x["date"])

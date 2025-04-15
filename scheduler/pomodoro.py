from datetime import datetime, timedelta
from scheduler.utils import parse_date

class PomodoroScheduler:
    def schedule(self, courses):
        today = datetime.today().date()
        schedule = []
        
        for course in sorted(courses, key=lambda c: parse_date(c['deadline'])):
            try:
                time_remaining = int(float(course["hours"])) * 60 # Convert hours to minutes
                deadline = parse_date(course["deadline"])
                days = (deadline - today).days + 1

                if deadline < today:
                    continue
            except (ValueError, KeyError):
                continue # Invalid input, skip this course
            
            current_day = today
            while time_remaining > 0:
                duration = min(25, time_remaining)
                schedule.append({
                    "course": course["course"],
                    "block": "study",
                    "duration": duration,
                    "date": str(current_day)
                })
                time_remaining -= duration
                if (current_day + timedelta(days=1)) > deadline:
                    current_day = today
                else:
                    current_day += timedelta(days=1)
                    
        return schedule

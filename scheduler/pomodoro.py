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
                
                if deadline < today:
                    continue
                
                date_range = [today + timedelta(days=i) for i in range((deadline - today).days + 1)]
                if len(date_range) == 0:
                    continue
                
            except (ValueError, KeyError):
                continue # Invalid input, skip this course
            
            date_index = 0
            while time_remaining > 0:
                duration = min(25, time_remaining)
                schedule.append({
                    "course": course["course"],
                    "block": "study",
                    "duration": duration,
                    "date": str(date_range[date_index])
                })
                time_remaining -= duration
                date_index = (date_index + 1) % len(date_range)
                    
        return schedule

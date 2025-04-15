from datetime import datetime, timedelta
from scheduler.utils import parse_date

class PomodoroScheduler:
    def schedule(self, courses):
        schedule = []
        
        for course in sorted(courses, key=lambda c: parse_date(c['deadline'])):
            try:
                time_remaining = int(float(course["hours"])) * 60 # Convert hours to minutes
                deadline = parse_date(course["deadline"])
                
                start_date = datetime.today().date()
                
                date_range = [start_date + timedelta(days=i) for i in range((deadline - start_date).days + 1)]
                
                if not date_range:
                    continue
                
                date_index = 0
            except (ValueError, KeyError) as err:
                print(f"Error processing course {course['course']}: {err}")
                continue # Invalid input, skip this course
            
            while time_remaining > 0:
                duration = min(25, time_remaining)
                assigned_date = date_range[date_index % len(date_range)]
                schedule.append({
                    "course": course["course"],
                    "block": "study",
                    "duration": duration,
                    "date": str(assigned_date)
                })
                time_remaining -= duration
                date_index += 1
                    
        return sorted(schedule, key=lambda x: x["date"])

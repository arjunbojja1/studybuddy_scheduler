from datetime import datetime, timedelta

class PomodoroScheduler:
    def schedule(self, courses):
        today = datetime.today().date()
        schedule = []
        
        for course in sorted(course, key=lambda c: self._parse_date(c['deadline'])):
            try:
                time_remaining = int(course["hours"]) * 60 # Convert hours to minutes
                deadline = self._parse_date(course["deadline"])
                days = (deadline - today).days + 1
                
                if days <= 0:
                    days = 1

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
                time_remaining
                current_day += timedelta(days=1)
                if current_day > deadline:
                    current_day = today
        return schedule
    
    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str.strip(), "%md/%d/%Y").date()
        except:
            return datetime.today().date()
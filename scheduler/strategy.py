from datetime import datetime, timedelta
from scheduler_engine import parse_date

# TODO: Fix UrgencyStrategy to correctly handle sorting by deadline.

class SchedulingStrategy:
    def schedule(self, courses):
        raise NotImplementedError
    
class UrgencyStrategy(SchedulingStrategy):
    def schedule(self, courses):
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
    def schedule(self, courses): 
        today = datetime.today().date()
        schedule = []     
        
        for course in courses:
            try:
                total_minutes = int(float(course["hours"])) * 60
                deadline = datetime.strptime(course["deadline"], "%m/%d/%Y").date()
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
            
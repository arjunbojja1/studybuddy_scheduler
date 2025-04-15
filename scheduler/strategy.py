from datetime import datetime, timedelta
from scheduler_engine import parse_date

# TODO: Fix UrgencyStrategy to correctly handle sorting by deadline.

class SchedulingStrategy:
    def schedule(self, courses):
        raise NotImplementedError
    
class UrgencyStrategy(SchedulingStrategy):
    def schedule(self, courses):
        
        def parse_deadline(deadline):
            try:
                return datetime.strptime(deadline.strip(), "%m/%d/%Y")
            except:
                return datetime.max
    
        sorted_courses = sorted(courses, key=lambda course: parse_deadline(course['deadline']))
        
        for c in sorted_courses:
            print(f"Course: {c['course']}, Deadline: {c['deadline']}")
        
        return [{"course": course['course'], "block": "study", "duration": int(course['hours']) * 60} for course in sorted_courses]
    
class EvenDistributionStrategy(SchedulingStrategy):
    def schedule(self, courses): 
        today = datetime.today().date()
        schedule = []     
        
        for course in sorted(courses, key=lambda c: parse_date(c['deadline'])):
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
            
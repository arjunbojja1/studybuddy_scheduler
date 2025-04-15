from datetime import datetime

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
        total_time = sum(int(course['hours']) for course in courses)
        
        if total_time == 0:
            return []
        
        return [
            {"course": course['course'], "block": "study", "duration": int(course['hours']) * 60}
            for course in courses
        ]
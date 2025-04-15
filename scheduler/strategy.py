from datetime import datetime

class SchedulingStrategy:
    def schedule(self, courses):
        raise NotImplementedError
    
class UrgencyStrategy(SchedulingStrategy):
    def schedule(self, courses):
        
        def parse_deadline(deadline):
            return datetime.strptime(deadline, "%Y-%m-%d")
        
        
        sorted_courses = sorted(courses, key=lambda course: course['deadline'])
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
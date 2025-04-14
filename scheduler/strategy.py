class SchedulingStrategy:
    def schedule(self, courses):
        raise NotImplementedError
    
class UrgencyStrategy(SchedulingStrategy):
    def schedule(self, courses):
        return sorted(courses, key=lambda course: course.deadline)
    
class EvenDistributionStrategy(SchedulingStrategy):
    def schedule(self, courses):
        total_time = sum(course.estimated_time for course in courses)
        return [
            {"name": course.name, "allocated_time": course.estimated_time / total_time * 100}
            for course in courses
        ]
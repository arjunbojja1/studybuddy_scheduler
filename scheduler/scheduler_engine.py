from scheduler.strategy import SchedulingStrategy

class SchedulerEngine:
    def __init__(self, courses, strategy):
        self.courses = courses
        self.strategy = strategy
        
    def generate_schedule(self):
        if not isinstance(self.strategy, SchedulingStrategy):
            raise ValueError("Invalid scheduling strategy")
        schedule = self.strategy.schedule(self.courses)
        print(f"Generated schedule: {schedule}")
        return schedule
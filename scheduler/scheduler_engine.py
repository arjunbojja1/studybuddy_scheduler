from scheduler.strategy import EvenDistributionStrategy
from scheduler.strategy import UrgencyStrategy
from scheduler.pomodoro import PomodoroScheduler

class SchedulerEngine:
    def __init__(self, strategy="even"):
        self.strategy = strategy
        
    def generate_schedule(self, courses):
        if self.strategy == "pomodoro":
            return PomodoroScheduler().schedule(courses)
        elif self.strategy == "even":
            return UrgencyStrategy().schedule(courses)
        elif self.strategy == "urgency":
            return EvenDistributionStrategy().schedule(courses)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
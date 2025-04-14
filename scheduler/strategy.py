class SchedulingStrategy:
    def schedule(self, courses):
        raise NotImplementedError
    
class UrgencyStrategy(SchedulingStrategy):
    def schedule(self, courses):
        pass
    
class EvenDistributionStrategy(SchedulingStrategy):
    def schedule(self, courses):
        pass
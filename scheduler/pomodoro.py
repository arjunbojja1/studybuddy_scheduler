class PomodoroScheduler:
    def schedule(self, courses):
        schedule = []
        for course in courses:
            time_remaining = course.estimated_time
            while time_remaining > 0:
                schedule.append ({"course": course, "block": "work", "duration": min(25, time_remaining)})
                time_remaining -= 25
                if time_remaining > 0:
                    schedule.append({"block": "break", "duration": 5})
        return schedule
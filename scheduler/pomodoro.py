class PomodoroScheduler:
    def schedule(self, courses):
        schedule = []
        for course in courses:
            try:
                time_remaining = int(course["hours"]) * 60 # Convert hours to minutes
            except (ValueError, KeyError):
                continue # Invalid input, skip this course
            
            pomodoro_count = 0
            while time_remaining > 0:
                work_time = min(25, time_remaining)
                schedule.append ({
                    "course": course["course"], 
                    "block": "work", 
                    "duration": work_time
                    })
                time_remaining -= work_time
                pomodoro_count += 1
                
                if time_remaining <= 0:
                    break
                
                if pomodoro_count % 4 == 0:
                    schedule.append({
                        "course": course["course"], 
                        "block": "long break", 
                        "duration": 15
                    })
                else:
                    schedule.append({
                        "course": course["course"], 
                        "block": "short break", 
                        "duration": 5
                    })
        return schedule
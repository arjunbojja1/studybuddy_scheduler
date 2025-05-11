import csv
from io import StringIO

class FileExporter:
    def export_to_csv(self, schedule, filename=None):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["course", "block", "duration", "date"])
        writer.writeheader()
        writer.writerows(schedule)
        return output.getvalue()
    
    def export_to_txt(self, schedule, filename=None):
        lines = [
            f"{entry['date']} | {entry['course']} | {entry['block']} | {entry['duration']} min"
            for entry in schedule
        ]
        return "\n".join(lines)
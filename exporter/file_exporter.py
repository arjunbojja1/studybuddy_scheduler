"""File exporter for the StudyBuddy Scheduler.

This script defines the FileExporter class, which exports schedules
to CSV and plain text formats.
"""

import csv
from io import StringIO

class FileExporter:
    """Exports schedules to CSV or plain text formats."""

    def export_to_csv(self, schedule, filename=None):
        """Exports the schedule to a CSV format.

        Args:
            schedule (list of dict): The schedule to export, where each dict
                contains 'course', 'block', 'duration', and 'date' keys.
            filename (str, optional): Filename to save the CSV. Defaults to None.

        Returns:
            str: The CSV content as a string.
        """
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["course", "block", "duration", "date"])
        writer.writeheader()
        writer.writerows(schedule)
        return output.getvalue()
    
    def export_to_txt(self, schedule, filename=None):
        """Exports the schedule to a plain text format.

        Args:
            schedule (list of dict): The schedule to export, where each dict
                contains 'course', 'block', 'duration', and 'date' keys.
            filename (str, optional): Filename to save the text file. Defaults to None.

        Returns:
            str: The plain text content as a string.
        """
        lines = [
            f"{entry['date']} | {entry['course']} | {entry['block']} | {entry['duration']} min"
            for entry in schedule
        ]
        return "\n".join(lines)
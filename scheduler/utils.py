"""Utility functions for the StudyBuddy Scheduler.

This script includes helper functions for parsing dates and generating
visualizations, such as pie charts for study durations.
"""

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import defaultdict

from datetime import datetime

def parse_date(date_str):
    """Parses a date string into a datetime.date object.

    Supports multiple date formats. If parsing fails, returns today's date.

    Args:
        date_str (str): The date string to parse.

    Returns:
        datetime.date: The parsed date or today's date if parsing fails.
    """
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
        except Exception as err:
            print(f"Error parsing date '{date_str}': {err}")
            return datetime.today().date()
        
def generate_pie_chart(blocks):
    """Generates a pie chart for study durations by course.

    Args:
        blocks (list of dict): List of schedule blocks, where each block
            contains 'course' and 'duration' keys.

    Returns:
        str: Base64-encoded PNG image of the pie chart.
    """
    durations = defaultdict(int)
    for block in blocks:
        durations[block["course"]] += block["duration"]

    labels = list(durations.keys())
    sizes = list(durations.values())
    colors = plt.cm.Set3.colors[:len(labels)]  # pretty colors

    fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
    ax.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140, colors=colors)
    ax.axis('equal')  # Equal aspect ratio for a perfect circle

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close(fig)
    buf.seek(0)

    return base64.b64encode(buf.read()).decode('utf-8')

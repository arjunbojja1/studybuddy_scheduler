import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import defaultdict

from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
        except Exception as err:
            print(f"Error parsing date '{date_str}': {err}")
            return datetime.today().date()
        
def generate_pie_chart(blocks):
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

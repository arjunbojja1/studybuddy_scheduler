from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y/%d/%Y").date()
    except Exception as err:
        print(f"Error parsing date {date_str}: {err}")
        return datetime.today().date()
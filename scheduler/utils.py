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
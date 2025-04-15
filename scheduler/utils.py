from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
    except:
        return datetime.today().date()
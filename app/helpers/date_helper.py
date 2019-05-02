
import datetime


def suffix(d):
    return str(d) + {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

def user_format(date: datetime.date):
    return date.strftime(f"%b {suffix(date.day)}, %Y")

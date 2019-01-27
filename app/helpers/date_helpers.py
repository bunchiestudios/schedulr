from isoweek import Week
from datetime import date
import re
from typing import Optional

def date_to_iso_week(date_str: str) -> Optional[Week]:
    # Both date formats are valid under ISO 8601
    date_full_regex = re.compile('^\\d{4}-\\d{2}-\\d{2}$')
    date_min_regex = re.compile('^\\d{8}$')

    if date_full_regex.match(date_str):
        split_date = [int(item) for item in date_str.split('-')]
        try:
            week_date = date(*split_date)
        except ValueError:
            return None
    elif date_min_regex.match(date_str):
        try:
            week_date = date(
                int(date_str[0:4]), int(date_str[4:6]), int(date_str[6:8])
            )
        except ValueError:
            return None
    else:
        return None
    return Week.withdate(week_date)


def iso_week_to_date(iso_week: Week) -> str:
    return iso_week.monday().isoformat()

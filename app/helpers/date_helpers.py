from typing import List

from isoweek import Week


def first_week_of_year(year: int) -> Week:
    return Week(year, 1)


def last_week_of_year(year: int) -> Week:
    # Some years have 53 weeks instead of 52 (ex. 2015). This covers that case
    return Week(year, 53) if Week(year, 53).year == year else Week(year, 52)


def all_weeks_between(start_week: Week, end_week: Week) -> List[Week]:
    """
    Returns all weeks between to given weeks, inclusive.
    :param start_week: Start iso week for the count, inclusive.
    :param end_week: End iso week for the count, inclusive.
    :returns: Return a list of weeks between the two weeks, inclusive
    """
    result = []
    curr_week = start_week

    while curr_week <= end_week:
        result.append(curr_week)
        curr_week += 1

    return result

from isoweek import Week


def first_week_of_year(year: int) -> Week:
    return Week(year, 1)


def last_week_of_year(year: int) -> Week:
    # Some years have 53 weeks instead of 52 (ex. 2015). This covers that case
    return Week(year, 53) if Week(year, 53).year == year else Week(year, 52)

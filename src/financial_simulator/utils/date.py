from calendar import monthrange, isleap
from datetime import date
from functools import cache

DAYS_IN_REGULAR_YEAR = 365
DAYS_IN_LEAP_YEAR = 366


def correct_day_of_the_month(day: int, current_date: date) -> int:
    _, days_in_month = monthrange(current_date.year, current_date.month)
    return days_in_month if day > days_in_month else day


@cache
def days_in_year(year: int) -> int:
    return DAYS_IN_LEAP_YEAR if isleap(year) else DAYS_IN_REGULAR_YEAR

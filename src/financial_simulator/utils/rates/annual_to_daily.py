from decimal import Decimal
from functools import cache


@cache
def annual_to_continuous_daily_rate(annual_rate: Decimal, days_in_year: int) -> Decimal:
    return ((1 + annual_rate) ** (1 / Decimal(days_in_year))) - 1


@cache
def annual_to_periodic_daily_rate(annual_rate: Decimal, period_count: int, days_in_year: int) -> Decimal:
    return ((period_count * ((1 + annual_rate) ** (1 / Decimal(period_count)) - 1)) /
            days_in_year)

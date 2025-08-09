from calendar import JANUARY
from dataclasses import dataclass
from datetime import date
from functools import cache

from .schedule import Schedule, Scheduled
from ..utils.date import correct_day_of_the_month


@dataclass(frozen=True)
class YearlySchedule(Schedule):
    month: int = JANUARY
    day: int = 1

    @cache
    def check(self, current_date: date) -> Scheduled:
        if current_date.month == self.month:
            if current_date.day == correct_day_of_the_month(self.day, current_date):
                return Scheduled(match=True, complete=False)
        return Scheduled(match=False, complete=False)

from dataclasses import dataclass
from datetime import date
from functools import cache

from .schedule import Schedule, Scheduled
from ..utils.date import correct_day_of_the_month


@dataclass(frozen=True)
class MonthlySchedule(Schedule):
    day: int = 1

    @cache
    def check(self, current_date: date) -> Scheduled:
        return Scheduled(match=current_date.day == correct_day_of_the_month(self.day, current_date),
                         complete=False)

from dataclasses import dataclass
from datetime import date
from functools import cache

from .schedule import Schedule, Scheduled


@dataclass(frozen=True)
class DaySchedule(Schedule):
    day: date = date.today()

    @cache
    def check(self, current_date: date) -> Scheduled:
        return Scheduled(match=self.day == current_date,
                         complete=self.day <= current_date)

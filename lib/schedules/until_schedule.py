from dataclasses import dataclass
from datetime import date, timedelta
from functools import cache

from .schedule import Schedule, Scheduled


@dataclass(frozen=True)
class UntilSchedule(Schedule):
    until_date: date = date.today()

    @cache
    def check(self, current_date: date) -> Scheduled:
        return Scheduled(match=current_date < self.until_date,
                         complete=current_date >= self.until_date - timedelta(days=1))

from dataclasses import dataclass
from datetime import date, timedelta
from functools import cache

from .schedule import Schedule, Scheduled


@dataclass(frozen=True)
class RangeSchedule(Schedule):
    from_date: date = date.today()
    until_date: date = date.today()

    @cache
    def check(self, current_date: date) -> Scheduled:
        return Scheduled(match=self.from_date <= current_date < self.until_date,
                         complete=current_date >= self.until_date - timedelta(days=1))

from dataclasses import dataclass
from datetime import date
from functools import cache

from .schedule import Schedule, Scheduled


@dataclass(frozen=True)
class DailySchedule(Schedule):
    @cache
    def check(self, current_date: date) -> Scheduled:
        return Scheduled(match=True,
                         complete=False)

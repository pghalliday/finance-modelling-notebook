from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import Callable

from .schedule import Schedule, Scheduled


@dataclass(frozen=True)
class FilterSchedule(Schedule):
    filter: Callable[[date], Scheduled]

    @cache
    def check(self, current_date: date) -> Scheduled:
        return self.filter(current_date)

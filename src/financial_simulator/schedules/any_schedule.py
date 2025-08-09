from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import Sequence

from .schedule import Schedule, Scheduled


@dataclass(frozen=True)
class AnySchedule(Schedule):
    schedules: Sequence[Schedule] = ()

    @cache
    def check(self, current_date: date) -> Scheduled:
        schedules_and_scheduled = tuple((schedule, schedule.check(current_date))
                                        for schedule
                                        in self.schedules)
        return Scheduled(match=any(scheduled.match for _schedule, scheduled in schedules_and_scheduled),
                         complete=all(scheduled.complete for _schedule, scheduled in schedules_and_scheduled))

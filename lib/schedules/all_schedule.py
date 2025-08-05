from dataclasses import dataclass
from datetime import date
from typing import Sequence

from .schedule import Schedule, Scheduled


@dataclass(frozen=True)
class AllSchedule(Schedule):
    schedules: Sequence[Schedule] = ()

    def check(self, current_date: date) -> Scheduled:
        schedules_and_scheduled = tuple((schedule, schedule.check(current_date))
                                        for schedule
                                        in self.schedules)
        return Scheduled(match=all(scheduled.match for _schedule, scheduled in schedules_and_scheduled),
                         complete=any(scheduled.complete for _schedule, scheduled in schedules_and_scheduled))

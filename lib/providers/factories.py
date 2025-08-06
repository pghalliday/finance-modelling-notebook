from datetime import date
from typing import TypeVar, Mapping

from .merge_provider import MergeProvider
from .provider import Provider
from .scheduled_provider import ScheduledProvider
from ..schedules import DaySchedule

T = TypeVar('T')


def create_sequence_provider(days: Mapping[date, T]) -> Provider[T]:
    return MergeProvider(providers=tuple(ScheduledProvider(schedule=DaySchedule(day),
                                                           value=value)
                                         for day, value in days.items()))

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Scheduled:
    match: bool = False
    complete: bool = False


class Schedule(metaclass=ABCMeta):
    @abstractmethod
    def check(self, current_date: date) -> Scheduled:
        raise NotImplementedError

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class EntityState:
    cash: float


class Entity(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'next') and
                callable(subclass.next) or
                NotImplemented)

    @abstractmethod
    def next(self, current_date: date, state: EntityState) -> EntityState:
        raise NotImplementedError

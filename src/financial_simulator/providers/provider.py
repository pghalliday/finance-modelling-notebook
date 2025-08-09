from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import TypeVar, Generic, Sequence

T = TypeVar('T')


@dataclass(frozen=True)
class Provided(Generic[T]):
    values: Sequence[T] = ()
    complete: bool = False


class Provider(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def get(self, current_date: date) -> Provided[T]:
        raise NotImplementedError

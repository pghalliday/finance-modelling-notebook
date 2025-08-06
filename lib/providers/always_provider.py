from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TypeVar

from .provider import Provider, Provided

T = TypeVar('T')


@dataclass(frozen=True)
class AlwaysProvider(Provider[T]):
    value: T = None

    @cache
    def get(self, current_date: date) -> Provided[T]:
        return Provided(values=(self.value,),
                        complete=False)

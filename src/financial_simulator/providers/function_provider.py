from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TypeVar, Callable

from .provider import Provider, Provided

T = TypeVar('T')


@dataclass(frozen=True)
class FunctionProvider(Provider[T]):
    function: Callable[[date], Provided[T]]

    @cache
    def get(self, current_date: date) -> Provided[T]:
        return self.function(current_date)

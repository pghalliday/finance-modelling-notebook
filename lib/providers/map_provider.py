from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TypeVar, Callable, Generic

from .never_provider import NeverProvider
from .provider import Provider, Provided

T = TypeVar('T')
U = TypeVar('U')


@dataclass(frozen=True)
class MapProvider(Generic[T, U], Provider[T]):
    transform: Callable[[U], T]
    provider: Provider[U] = NeverProvider()

    @cache
    def get(self, current_date: date) -> Provided[T]:
        provided = self.provider.get(current_date)
        return Provided(values=tuple(self.transform(value) for value in provided.values),
                        complete=provided.complete)

from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TypeVar, Callable, Generic, Sequence

from .never_provider import NeverProvider
from .provider import Provider, Provided

T = TypeVar('T')
U = TypeVar('U')


@dataclass(frozen=True)
class FlatMapProvider(Generic[T, U], Provider[T]):
    transform: Callable[[U], Sequence[T]]
    provider: Provider[U] = NeverProvider()

    @cache
    def get(self, current_date: date) -> Provided[T]:
        provided = self.provider.get(current_date)
        return Provided(values=tuple(t_value
                                     for sequence in (self.transform(u_value)
                                                      for u_value
                                                      in provided.values)
                                     for t_value in sequence),
                        complete=provided.complete)

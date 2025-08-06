from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TypeVar, Sequence

from .provider import Provider, Provided

T = TypeVar('T')


@dataclass(frozen=True)
class MergeProvider(Provider[T]):
    providers: Sequence[Provider[T]] = ()

    @cache
    def get(self, current_date: date) -> Provided[T]:
        providers_and_provided = tuple((provider, provider.get(current_date))
                                       for provider
                                       in self.providers)
        return Provided(values=tuple(value
                                     for sub_values in [provided.values
                                                        for _provider, provided in
                                                        providers_and_provided]
                                     for value in sub_values),
                        complete=all(provided.complete for _provider, provided in providers_and_provided))

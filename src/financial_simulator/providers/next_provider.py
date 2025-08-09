from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TypeVar, Sequence

from .provider import Provider, Provided

T = TypeVar('T')


@dataclass(frozen=True)
class NextProvider(Provider[T]):
    providers: Sequence[Provider[T]] = ()

    @cache
    def get(self, current_date: date) -> T:
        providers_and_provided = tuple((provider, provider.get(current_date))
                                       for provider
                                       in self.providers)
        return Provided(values=next((sub_values
                                     for sub_values
                                     in [provided.values
                                         for _provider, provided
                                         in providers_and_provided]
                                     if sub_values), tuple()),
                        complete=all(provided.complete for _provider, provided in providers_and_provided))

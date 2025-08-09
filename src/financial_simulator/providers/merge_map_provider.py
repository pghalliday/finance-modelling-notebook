from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TypeVar, Callable, Generic, Sequence

from .never_provider import NeverProvider
from .provider import Provider, Provided

T = TypeVar('T')
U = TypeVar('U')


@dataclass(frozen=True)
class MergeMapProvider(Generic[T, U], Provider[T]):
    transform: Callable[[date, U], Provider[T]]
    provider: Provider[U] = NeverProvider()
    __sub_providers: Sequence[Provider[T]] = ()

    @cache
    def get(self, current_date: date) -> Provided[T]:
        # first, get the provided sequence of U
        provided = self.provider.get(current_date)
        # for each U, transform to a new Provider
        sub_providers = tuple(self.transform(current_date, value) for value in provided.values)
        self.__sub_providers += sub_providers
        providers_and_provided = tuple((provider, provider.get(current_date))
                                       for provider
                                       in self.__sub_providers)
        self.__sub_providers = tuple(provider
                                     for provider, provided in providers_and_provided
                                     if not provided.complete)
        return Provided(values=tuple(value
                                     for sub_values in [provided.values
                                                        for _provider, provided in
                                                        providers_and_provided]
                                     for value in sub_values),
                        complete=provided.complete and not self.__sub_providers)

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Tuple, TypeVar, Mapping, Sequence

T = TypeVar('T')


@dataclass(frozen=True)
class Band:
    lower: Decimal
    size: Decimal | None

    def __post_init__(self):
        if self.lower < Decimal('0.0'):
            raise ValueError('Lower bound must be greater than or equal to 0.0')

    def __str__(self):
        if self.lower == Decimal('0.0'):
            return 'always' if self.size is None else f'up to {self.lower + self.size:.2f}'
        return f'above {self.lower:.2f}' if self.size is None else f'from {self.lower:.2f} to {self.lower + self.size:.2f}'

    def portion(self, amounts: List[Decimal]) -> List[Decimal]:
        total = sum(amounts)
        remainder = total - self.lower
        if remainder > Decimal('0.0'):
            unallocated = -self.lower
            to_allocate = remainder if self.size is None else min(remainder, self.size)
            portions: List[Decimal] = []
            for amount in amounts:
                unallocated += amount
                if unallocated > Decimal('0.0'):
                    portion = min(to_allocate, unallocated, amount)
                    portions.append(portion)
                    to_allocate -= portion
                else:
                    portions.append(Decimal('0.0'))
            return portions
        else:
            return [Decimal('0.0')] * len(amounts)


def create_bands(raw_bands: Mapping[Decimal, T]) -> Sequence[Tuple[Band, T]]:
    bands = []
    sorted_bands = sorted(raw_bands.items())
    last_value: T | None = None
    last_above: Decimal | None = None
    for above, value in sorted_bands:
        if last_value is not None:
            bands.append((Band(lower=last_above, size=above - last_above), last_value))
        last_value = value
        last_above = above
    bands.append((Band(lower=last_above, size=None), last_value))
    return tuple(bands)

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from functools import cache
from typing import Tuple, Sequence, Mapping

from prettytable import PrettyTable, TableStyle

from .rate import Rate, RateCalculation
from ..utils.bands import Band, create_bands
from ..utils.format import format_day


@dataclass(frozen=True)
class BandedRateCalculation(RateCalculation):
    rate: BandedRate
    calculations: Sequence[RateCalculation]

    @cache
    def __str__(self):
        table = PrettyTable(['Band', 'Rate', 'Balance', 'Accrued', 'Calculation'])
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_rows([[str(band),
                         str(rate),
                         f'{calculation.balance:.6f}',
                         f'{calculation.accrued:.6f}',
                         f'{calculation.calculation:.6f}']
                        for (band, rate), calculation
                        in zip(self.rate.bands, self.calculations)])
        table.add_divider()
        table.add_row([format_day(self.current_date),
                       'Totals',
                       f'{self.balance:.6f}',
                       f'{self.accrued:.6f}',
                       f'{self.calculation:.6f}'])
        table.align['Band'] = 'l'
        table.align['Rate'] = 'r'
        table.align['Balance'] = 'r'
        table.align['Accrued'] = 'r'
        table.align['Calculation'] = 'r'
        return table.get_string()


@dataclass(frozen=True)
class BandedRate(Rate):
    bands: Sequence[Tuple[Band, Rate]] = ()

    @cache
    def __str__(self):
        table = PrettyTable(['Band', 'Rate'])
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_rows([[str(band), str(rate)] for band, rate in self.bands])
        table.align['Band'] = 'l'
        table.align['Rate'] = 'r'
        return table.get_string()

    @cache
    def calculate(self, current_date: date, balance: Decimal, accrued: Decimal) -> BandedRateCalculation:
        calculations = tuple(rate.calculate(current_date, *(band.portion([balance, accrued])))
                             for band, rate
                             in self.bands)
        return BandedRateCalculation(rate=self,
                                     current_date=current_date,
                                     balance=balance,
                                     accrued=accrued,
                                     calculation=Decimal(
                                         sum([calculation.calculation for calculation in calculations])),
                                     calculations=calculations)


def create_banded_rate(raw_bands: Mapping[Decimal, Rate]) -> BandedRate:
    return BandedRate(create_bands(raw_bands))

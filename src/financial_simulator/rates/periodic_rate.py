from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from functools import cache

from prettytable import PrettyTable, TableStyle

from .rate import Rate, RateCalculation
from ..utils.date import days_in_year
from ..utils.format import format_day
from ..utils.rates import annual_to_periodic_daily_rate


@dataclass(frozen=True)
class PeriodicRateCalculation(RateCalculation):
    rate: PeriodicRate
    daily_rate: Decimal

    @cache
    def __str__(self):
        table = PrettyTable(['label', 'value'])
        table.add_row(['Current date', format_day(self.current_date)])
        table.add_row(['Rate', str(self.rate)])
        table.add_row(['Daily rate', f'{self.daily_rate * 100:.6f}'])
        table.add_row(['Balance', f'{self.balance:.6f}'])
        table.add_row(['Accrued', f'{self.accrued:.6f}'])
        table.add_row(['Calculation', f'{self.calculation:.6f}'])
        table.set_style(TableStyle.SINGLE_BORDER)
        table.align['label'] = 'l'
        table.align['value'] = 'r'
        table.header = False
        return table.get_string()


@dataclass(frozen=True)
class PeriodicRate(Rate):
    annual_rate: Decimal = Decimal('0.0')
    period_count: int = 1

    @cache
    def __str__(self):
        return f'PeriodicRate: {self.period_count} periods: {self.annual_rate * 100:.2f}%'

    @cache
    def calculate(self, current_date: date, balance: Decimal, accrued: Decimal) -> PeriodicRateCalculation:
        daily_rate = annual_to_periodic_daily_rate(self.annual_rate,
                                                   self.period_count,
                                                   days_in_year(current_date.year))
        return PeriodicRateCalculation(rate=self,
                                       current_date=current_date,
                                       daily_rate=daily_rate,
                                       balance=balance,
                                       accrued=accrued,
                                       calculation=daily_rate * balance)

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class RateCalculation:
    rate: Rate
    current_date: date
    balance: Decimal
    accrued: Decimal
    calculation: Decimal


@dataclass(frozen=True)
class Rate(metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, current_date: date, balance: Decimal, accrued: Decimal) -> RateCalculation:
        raise NotImplementedError

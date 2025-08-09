from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from ..rates import RateCalculation


@dataclass(frozen=True)
class InterestAccrual:
    accrual_date: date
    rate_calculation: RateCalculation
    new_interest_accrued: Decimal

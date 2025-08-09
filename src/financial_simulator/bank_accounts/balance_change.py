from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class BalanceChange:
    change_date: date
    source: str
    amount: Decimal
    new_balance: Decimal

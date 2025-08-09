from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class InterestApplication:
    application_date: date
    amount: Decimal
    new_interest_applied: Decimal

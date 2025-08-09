from calendar import JANUARY, APRIL, JULY, OCTOBER
from dataclasses import replace
from datetime import date
from decimal import Decimal

from .state import State
from ....providers import ScheduledProvider, NextProvider, AlwaysProvider
from ....schedules import YearlySchedule, AnySchedule


def payout(current_date: date, state: State) -> State:
    return replace(state,
                   current_date=current_date,
                   interest_paid=state.interest_paid + state.interest_accrued,
                   interest_accrued=Decimal('0.0'))


def accrue(current_date: date, state: State) -> State:
    return replace(state,
                   current_date=current_date)


ANNUAL_PAYMENT_SCHEDULE = YearlySchedule(JANUARY, 1)
ANNUAL_UPDATER_PROVIDER = NextProvider((ScheduledProvider(payout, ANNUAL_PAYMENT_SCHEDULE),
                                        AlwaysProvider(accrue)))

QUARTERLY_PAYMENT_SCHEDULE = AnySchedule((YearlySchedule(APRIL, 1),
                                          YearlySchedule(JULY, 1),
                                          YearlySchedule(OCTOBER, 1),
                                          YearlySchedule(JANUARY, 1)))
QUARTERLY_UPDATER_PROVIDER = NextProvider((ScheduledProvider(payout, QUARTERLY_PAYMENT_SCHEDULE),
                                           AlwaysProvider(accrue)))

DAILY_UPDATER_PROVIDER = AlwaysProvider(payout)

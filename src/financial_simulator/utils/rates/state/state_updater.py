from dataclasses import replace
from datetime import date
from typing import Callable

from .state import State
from ....providers import Provider
from ....rates import Rate


class StateUpdater(object):
    rate: Rate
    updater_provider: Provider[Callable[[date, State], State]]

    def __init__(self,
                 calculator: Rate,
                 updater_provider: Provider[Callable[[date, State], State]]):
        self.rate = calculator
        self.updater_provider = updater_provider

    def update(self, current_date: date, state: State) -> State:
        # apply the payment schedule first
        state = self.updater_provider.get(current_date).values[0](current_date, state)
        # calculate the accrual
        calculation = self.rate.calculate(current_date,
                                          state.net_deposits + state.interest_paid,
                                          state.interest_accrued)
        # then apply the rate and accrue
        return replace(state,
                       interest_accrued=state.interest_accrued + calculation.calculation)

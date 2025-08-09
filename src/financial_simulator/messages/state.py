from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, timedelta
from typing import Tuple, Sequence

from financial_simulator.messages.message import Message


@dataclass(frozen=True)
class State:
    current_date: date

    def on_day(self, current_date: date) -> Tuple[State, Sequence[Message]]:
        assert current_date == current_date + timedelta(
            days=1), f"Must call on_day with successive days: previous day: {self.current_date}: provided day: {current_date}"
        return replace(self, current_date=current_date), ()

    def on_message(self, message: Message) -> Tuple[State, Sequence[Message]]:
        return self, ()

from datetime import date

from src.financial_simulator.schedules.schedule import Schedule


class Amount(object):
    amount: float
    schedule: Schedule

    def __init__(self, amount: float, schedule: Schedule):
        self.amount = amount
        self.schedule = schedule

    def next(self, current_date: date) -> float:
        return self.amount if self.schedule.check(current_date) else 0.0

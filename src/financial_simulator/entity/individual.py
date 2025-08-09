from dataclasses import dataclass
from datetime import date
from typing import Dict

from src.financial_simulator import Asset
from src.financial_simulator import Schedule
from src.financial_simulator.entity.entity import Entity, EntityState
from src.financial_simulator.salaries.salary import Salary, sum_salary_payments


@dataclass(frozen=True)
class IndividualState(EntityState):
    box_1_taxable_income: float
    box_1_tax_paid: float


class Individual(Entity):
    salaries: Dict[str, Salary]
    revenue_schedule: Schedule
    expense_schedule: Schedule
    assets: Dict[str, Asset]

    def __init__(self,
                 salaries: Dict[str, Salary] = None,
                 revenue_schedule: Schedule = None,
                 expense_schedule: Schedule = None,
                 assets: Dict[str, Asset] = None):
        if salaries is None:
            salaries = {}
        if assets is None:
            assets = {}
        self.salaries = salaries
        self.revenue_schedule = revenue_schedule
        self.expense_schedule = expense_schedule
        self.assets = assets

    def next(self, current_date: date, state: IndividualState) -> IndividualState:
        total_salary_payment = sum_salary_payments([salary.next(current_date) for salary in self.salaries.values()])
        return IndividualState(
            cash=state.cash + total_salary_payment.net,
            box_1_taxable_income=state.box_1_taxable_income + total_salary_payment.gross,
            box_1_tax_paid=state.box_1_taxable_income + total_salary_payment.wage_tax,
        )

from datetime import date

from src.financial_simulator.salaries.salary import Salary, SalaryPayment, ZERO_SALARY_PAYMENT
from src.financial_simulator.utils.date import correct_day_of_the_month


class SimpleMonthlySalary(Salary):
    day: int
    net: float
    health_insurance: float
    wage_tax: float

    def __init__(self, day: int, net: float, health_insurance: float, wage_tax: float):
        self.day = day
        self.net = net
        self.health_insurance = health_insurance
        self.wage_tax = wage_tax

    def next(self, current_date: date) -> SalaryPayment:
        if current_date.day == correct_day_of_the_month(self.day, current_date):
            return SalaryPayment(gross=self.net + self.health_insurance + self.wage_tax,
                                 net=self.net,
                                 health_insurance=self.health_insurance,
                                 wage_tax=self.wage_tax)
        return ZERO_SALARY_PAYMENT

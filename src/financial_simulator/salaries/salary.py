from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date
from functools import reduce
from typing import List


@dataclass(frozen=True)
class SalaryPayment:
    gross: float
    net: float
    health_insurance: float
    wage_tax: float


ZERO_SALARY_PAYMENT = SalaryPayment(gross=0.0,
                                    net=0.0,
                                    health_insurance=0.0,
                                    wage_tax=0.0)


def sum_salary_payments(salary_payments: List[SalaryPayment]) -> SalaryPayment:
    return reduce(lambda x, y: SalaryPayment(gross=x.gross + y.gross,
                                             net=x.net + y.net,
                                             health_insurance=x.health_insurance + y.health_insurance,
                                             wage_tax=x.wage_tax + y.wage_tax),
                  salary_payments, ZERO_SALARY_PAYMENT)


class Salary(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'next') and
                callable(subclass.next) or
                NotImplemented)

    @abstractmethod
    def next(self, current_date: date) -> SalaryPayment:
        raise NotImplementedError

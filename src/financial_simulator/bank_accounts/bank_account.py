from __future__ import annotations

from calendar import JANUARY, DECEMBER
from dataclasses import dataclass, replace
from datetime import date, timedelta
from decimal import Decimal
from types import MappingProxyType
from typing import Sequence, Mapping, Tuple

from prettytable import PrettyTable, TableStyle

from .balance_change import BalanceChange
from .interest_accrual import InterestAccrual
from .interest_application import InterestApplication
from ..providers import Provider, NeverProvider
from ..rates import Rate
from ..schedules import Schedule, NeverSchedule
from ..utils.format import format_day


@dataclass(frozen=True)
class BankAccountProviders:
    rate_provider: Provider[Rate] = NeverProvider()
    interest_payment_schedule: Schedule = NeverSchedule()
    deposit_provider: Provider[Tuple[str, Decimal]] = NeverProvider()
    withdrawal_provider: Provider[Tuple[str, Decimal]] = NeverProvider()


@dataclass(frozen=True)
class BankAccount:
    current_date: date = date.today()
    balance_changes: Sequence[BalanceChange] = ()
    interest_applications: Sequence[InterestApplication] = ()
    interest_accruals: Sequence[InterestAccrual] = ()
    balance: Decimal = Decimal('0.0')
    interest_applied: Decimal = Decimal('0.0')
    interest_accrued: Decimal = Decimal('0.0')
    closing_balance: Mapping[int, Decimal] = MappingProxyType({})
    opening_balance: Mapping[int, Decimal] = MappingProxyType({})
    closing_interest_applied: Mapping[int, Decimal] = MappingProxyType({})
    opening_interest_applied: Mapping[int, Decimal] = MappingProxyType({})
    closing_interest_accrued: Mapping[int, Decimal] = MappingProxyType({})
    opening_interest_accrued: Mapping[int, Decimal] = MappingProxyType({})

    def __str__(self):
        table = PrettyTable(['label', 'value'])
        table.add_row(['Current date', format_day(self.current_date)])
        table.add_row(['Interest applied', f'{self.interest_applied:.6f}'])
        table.add_row(['Interest accrued', f'{self.interest_accrued:.6f}'])
        table.add_row(['Balance', f'{self.balance:.6f}'])
        table.add_row(['Total', f'{self.balance + self.interest_accrued:.6f}'])
        table.set_style(TableStyle.SINGLE_BORDER)
        table.align['label'] = 'l'
        table.align['value'] = 'r'
        table.header = False
        return table.get_string()

    def next_day(self) -> BankAccount:
        return replace(self, current_date=self.current_date + timedelta(days=1))

    def open_year(self) -> BankAccount:
        if self.current_date.month == JANUARY and self.current_date.day == 1:
            return replace(self,
                           opening_balance=MappingProxyType(
                               dict(self.opening_balance) | {self.current_date.year: self.balance}),
                           opening_interest_applied=MappingProxyType(
                               dict(self.opening_interest_applied) | {self.current_date.year: self.interest_applied}),
                           opening_interest_accrued=MappingProxyType(
                               dict(self.opening_interest_accrued) | {self.current_date.year: self.interest_accrued}))
        return self

    def close_year(self) -> BankAccount:
        if self.current_date.month == DECEMBER and self.current_date.day == 31:
            return replace(self,
                           closing_balance=MappingProxyType(
                               dict(self.closing_balance) | {self.current_date.year: self.balance}),
                           closing_interest_applied=MappingProxyType(
                               dict(self.closing_interest_applied) | {self.current_date.year: self.interest_applied}),
                           closing_interest_accrued=MappingProxyType(
                               dict(self.closing_interest_accrued) | {self.current_date.year: self.interest_accrued}))
        return self

    def apply_interest(self, interest_payment_schedule: Schedule) -> BankAccount:
        if interest_payment_schedule.check(self.current_date).match:
            new_interest_applied = self.interest_applied + self.interest_accrued
            new_balance = self.balance + self.interest_accrued
            return replace(self,
                           interest_applied=new_interest_applied,
                           interest_applications=tuple(self.interest_applications) + (
                               InterestApplication(application_date=self.current_date,
                                                   amount=self.interest_accrued,
                                                   new_interest_applied=new_interest_applied),),
                           balance=new_balance,
                           balance_changes=tuple(self.balance_changes) + (BalanceChange(change_date=self.current_date,
                                                                                        source='Interest',
                                                                                        amount=self.interest_accrued,
                                                                                        new_balance=new_balance),),
                           interest_accrued=Decimal('0.0'))
        return self

    def apply_deposit(self, label: str, amount: Decimal) -> BankAccount:
        new_balance = self.balance + amount
        return replace(self,
                       balance=new_balance,
                       balance_changes=tuple(self.balance_changes) + (
                           BalanceChange(change_date=self.current_date,
                                         source=f'Deposit: {label}',
                                         amount=amount,
                                         new_balance=new_balance),))

    def apply_deposits(self, provider: Provider[Tuple[str, Decimal]]) -> BankAccount:
        state = self
        for label, amount in provider.get(self.current_date).values:
            state = state.apply_deposit(label, amount)
        return state

    def apply_withdrawal(self, label: str, amount: Decimal) -> BankAccount:
        new_balance = self.balance - amount
        return replace(self,
                       balance=new_balance,
                       balance_changes=tuple(self.balance_changes) + (
                           BalanceChange(change_date=self.current_date,
                                         source=f'Withdrawal: {label}',
                                         amount=-amount,
                                         new_balance=new_balance),))

    def apply_withdrawals(self, provider: Provider[Tuple[str, Decimal]]) -> BankAccount:
        state = self
        for label, amount in provider.get(self.current_date).values:
            state = state.apply_withdrawal(label, amount)
        return state

    def accrue_interest(self, provider: Provider[Rate]) -> BankAccount:
        rates = provider.get(self.current_date).values
        if rates:
            rate_calculation = rates[0].calculate(self.current_date, self.balance,
                                                  self.interest_accrued)
            new_interest_accrued = self.interest_accrued + rate_calculation.calculation
            return replace(self,
                           interest_accrued=new_interest_accrued,
                           interest_accruals=tuple(self.interest_accruals) + (
                               InterestAccrual(accrual_date=self.current_date,
                                               rate_calculation=rate_calculation,
                                               new_interest_accrued=new_interest_accrued),))
        return self

    def next(self, providers: BankAccountProviders) -> BankAccount:
        return (self
                # add one day to the current date
                .next_day()
                # If at the start of the year then open the year
                .open_year()
                # Apply the accrued interest if it is an interest payment day
                .apply_interest(providers.interest_payment_schedule)
                # Check for deposits
                .apply_deposits(providers.deposit_provider)
                # Check for withdrawals
                .apply_withdrawals(providers.withdrawal_provider)
                # Calculate interest on the new balance
                .accrue_interest(providers.rate_provider)
                # If at the end of the year then close the year
                .close_year())

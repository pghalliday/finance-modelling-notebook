# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Bank Accounts
#
# State and reducer implementations to keep track of bank account changes.

# %%
from datetime import date
from decimal import Decimal, getcontext, FloatOperation

from financial_simulator.bank_accounts import BankAccount, BankAccountProviders
from financial_simulator.providers import AlwaysProvider
from financial_simulator.rates import ContinuousRate
from financial_simulator.schedules import DailySchedule
from financial_simulator.utils.date import days_in_year

decimal_context = getcontext()
decimal_context.traps[FloatOperation] = True
decimal_context.prec = 1000

# Start on the last day of last year so we create opening states for the first year in our range
START_DATE = date(date.today().year - 1, 12, 31)
# List 3 years from this year
YEARS = [START_DATE.year + offset for offset in range(1, 4)]
# Total number of days in years plus one, so we roll over into another year and create closing states
# for the last year in our range
DAYS = range(sum([days_in_year(year) for year in YEARS]) + 1)
RATE_PROVIDER = AlwaysProvider(ContinuousRate(Decimal('0.015')))
STARTING_BALANCE = Decimal('10_000')

INITIAL_STATE = BankAccount(current_date=START_DATE,
                            balance=STARTING_BALANCE)

print(f'Decimal context: {decimal_context}')
print(INITIAL_STATE)

# %% [markdown]
# The reducer should be provided with an interest rate and an interest payment schedule.

# %%
providers = BankAccountProviders(rate_provider=RATE_PROVIDER,
                                 interest_payment_schedule=DailySchedule())
state = INITIAL_STATE
for day in DAYS:
    state = state.next(providers)
print(state)

# %% [markdown]
# The state will also provide information on yearly opening and closing balances, etc.

# %%
for year in YEARS:
    print(f'Opening balance for year {year}: {state.opening_balance[year]:.6f}')
    print(f'Closing balance for year {year}: {state.closing_balance[year]:.6f}')
    balance_change = state.closing_balance[year] - state.opening_balance[year]
    print(f'Balance change for year {year}: {balance_change:.6f}')
    print()
    print(f'Opening interest applied for year {year}: {state.opening_interest_applied[year]:.6f}')
    print(f'Closing interest applied for year {year}: {state.closing_interest_applied[year]:.6f}')
    interest_applied_change = state.closing_interest_applied[year] - state.opening_interest_applied[year]
    print(f'Interest applied change for year {year}: {interest_applied_change:.6f}')
    print()
    print(f'Opening interest accrued for year {year}: {state.opening_interest_accrued[year]:.6f}')
    print(f'Closing interest accrued for year {year}: {state.closing_interest_accrued[year]:.6f}')
    interest_accrued_change = state.closing_interest_accrued[year] - state.opening_interest_accrued[year]
    print(f'Interest accrued change for year {year}: {interest_accrued_change:.6f}')
    print()
    interest_change = interest_applied_change + interest_accrued_change
    print(f'Interest change for year {year}: {interest_change:.6f}')
    print()

# Bank Accounts

State and reducer implementations to keep track of bank account changes.

```python
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
```

    Decimal context: Context(prec=1000, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[], traps=[InvalidOperation, DivisionByZero, FloatOperation, Overflow])
    ┌──────────────────┬──────────────────┐
    │ Current date     │ 2024-12-31 : Tue │
    │ Interest applied │         0.000000 │
    │ Interest accrued │         0.000000 │
    │ Balance          │     10000.000000 │
    │ Total            │     10000.000000 │
    └──────────────────┴──────────────────┘

The reducer should be provided with an interest rate and an interest payment schedule.

```python
providers = BankAccountProviders(rate_provider=RATE_PROVIDER,
                                 interest_payment_schedule=DailySchedule())
state = INITIAL_STATE
for day in DAYS:
    state = state.next(providers)
print(state)
```

    ┌──────────────────┬──────────────────┐
    │ Current date     │ 2028-01-01 : Sat │
    │ Interest applied │       456.783750 │
    │ Interest accrued │         0.425383 │
    │ Balance          │     10456.783750 │
    │ Total            │     10457.209133 │
    └──────────────────┴──────────────────┘

The state will also provide information on yearly opening and closing balances, etc.

```python
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
```

    Opening balance for year 2025: 10000.000000
    Closing balance for year 2025: 10149.585983
    Balance change for year 2025: 149.585983
    
    Opening interest applied for year 2025: 0.000000
    Closing interest applied for year 2025: 149.585983
    Interest applied change for year 2025: 149.585983
    
    Opening interest accrued for year 2025: 0.000000
    Closing interest accrued for year 2025: 0.414017
    Interest accrued change for year 2025: 0.414017
    
    Interest change for year 2025: 150.000000
    
    Opening balance for year 2026: 10149.585983
    Closing balance for year 2026: 10301.829772
    Balance change for year 2026: 152.243790
    
    Opening interest applied for year 2026: 149.585983
    Closing interest applied for year 2026: 301.829772
    Interest applied change for year 2026: 152.243790
    
    Opening interest accrued for year 2026: 0.414017
    Closing interest accrued for year 2026: 0.420228
    Interest accrued change for year 2026: 0.006210
    
    Interest change for year 2026: 152.250000
    
    Opening balance for year 2027: 10301.829772
    Closing balance for year 2027: 10456.357219
    Balance change for year 2027: 154.527447
    
    Opening interest applied for year 2027: 301.829772
    Closing interest applied for year 2027: 456.357219
    Interest applied change for year 2027: 154.527447
    
    Opening interest accrued for year 2027: 0.420228
    Closing interest accrued for year 2027: 0.426531
    Interest accrued change for year 2027: 0.006303
    
    Interest change for year 2027: 154.533750
    


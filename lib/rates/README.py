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

# %% [markdown] papermill={"duration": 0.008725, "end_time": "2025-08-06T12:37:03.562857", "exception": false, "start_time": "2025-08-06T12:37:03.554132", "status": "completed"}
# # Rates
#
# A collection of daily rate calculation algorithms.

# %% papermill={"duration": 0.052842, "end_time": "2025-08-06T12:37:03.620943", "exception": false, "start_time": "2025-08-06T12:37:03.568101", "status": "completed"}
from datetime import date, timedelta
from decimal import Decimal, getcontext, FloatOperation
from functools import reduce

from lib.rates import \
    ContinuousRate, \
    PeriodicRate, \
    create_banded_rate
from lib.utils.date import days_in_year
from lib.utils.rates.state import \
    State, \
    StateUpdater, \
    ANNUAL_UPDATER_PROVIDER, \
    QUARTERLY_UPDATER_PROVIDER, \
    DAILY_UPDATER_PROVIDER

decimal_context = getcontext()
decimal_context.traps[FloatOperation] = True
decimal_context.prec = 1000

START_DATE = date(date.today().year, 1, 1)
DAYS = [START_DATE + timedelta(days=day) for day in range(days_in_year(START_DATE.year))]
RATE = Decimal('0.015')
BANDS = {Decimal('0.0'): Decimal('0.10'),
         Decimal('1000.0'): Decimal('0.20'),
         Decimal('2000.0'): Decimal('0.30'),
         Decimal('3000.0'): Decimal('0.40'),
         Decimal('4000.0'): Decimal('0.0')}
STARTING_BALANCE = Decimal('10_000')

INITIAL_STATE = State(current_date=START_DATE - timedelta(days=1),
                      net_deposits=STARTING_BALANCE,
                      interest_paid=Decimal('0.0'),
                      interest_accrued=Decimal('0.0'))

print(f'Decimal context: {decimal_context}')
print(INITIAL_STATE)

# %% [markdown] papermill={"duration": 0.001833, "end_time": "2025-08-06T12:37:03.624973", "exception": false, "start_time": "2025-08-06T12:37:03.623140", "status": "completed"}
# ## ContinuousRate
#
# This calculator applies a continuously compounding algorithm, which most accurately reflects a
# continuous return given a desired annual rate.

# %% [markdown] papermill={"duration": 0.001874, "end_time": "2025-08-06T12:37:03.628759", "exception": false, "start_time": "2025-08-06T12:37:03.626885", "status": "completed"}
# Each call to calculate will return the daily amount associated with the given annual rate.

# %% papermill={"duration": 0.028346, "end_time": "2025-08-06T12:37:03.658733", "exception": false, "start_time": "2025-08-06T12:37:03.630387", "status": "completed"}
rate = ContinuousRate(RATE)
calculation = rate.calculate(current_date=START_DATE,
                             balance=STARTING_BALANCE,
                             accrued=Decimal('0.0'))
print(calculation)

# %% [markdown] papermill={"duration": 0.001373, "end_time": "2025-08-06T12:37:03.661745", "exception": false, "start_time": "2025-08-06T12:37:03.660372", "status": "completed"}
# So collecting the daily amounts over a full year, we can see the compounded result.

# %% papermill={"duration": 0.020139, "end_time": "2025-08-06T12:37:03.683231", "exception": false, "start_time": "2025-08-06T12:37:03.663092", "status": "completed"}
state_updater = StateUpdater(rate, ANNUAL_UPDATER_PROVIDER)
final_state = reduce(lambda state, day: state_updater.update(day, state), DAYS, INITIAL_STATE)
print(final_state)

# %% papermill={"duration": 0.018715, "end_time": "2025-08-06T12:37:03.703546", "exception": false, "start_time": "2025-08-06T12:37:03.684831", "status": "completed"}
state_updater = StateUpdater(rate, QUARTERLY_UPDATER_PROVIDER)
final_state = reduce(lambda state, day: state_updater.update(day, state), DAYS, INITIAL_STATE)
print(final_state)

# %% papermill={"duration": 0.018516, "end_time": "2025-08-06T12:37:03.723670", "exception": false, "start_time": "2025-08-06T12:37:03.705154", "status": "completed"}
state_updater = StateUpdater(rate, DAILY_UPDATER_PROVIDER)
final_state = reduce(lambda state, day: state_updater.update(day, state), DAYS, INITIAL_STATE)
print(final_state)

# %% [markdown] papermill={"duration": 0.002101, "end_time": "2025-08-06T12:37:03.727380", "exception": false, "start_time": "2025-08-06T12:37:03.725279", "status": "completed"}
# ## PeriodicRate
#
# This calculator applies a periodic compounding algorithm by applying the same rate to the
# balance for each day without taking into account the unrealized accrued amount. For a constant
# balance, this should provide the same return as the `ContinuousRate`. However,
# for a falling balance it will return less and for a rising balance it will return more.

# %% [markdown] papermill={"duration": 0.00196, "end_time": "2025-08-06T12:37:03.730900", "exception": false, "start_time": "2025-08-06T12:37:03.728940", "status": "completed"}
# Each call to calculate will return the daily amount associated with the given annual rate.

# %% papermill={"duration": 0.004508, "end_time": "2025-08-06T12:37:03.736851", "exception": false, "start_time": "2025-08-06T12:37:03.732343", "status": "completed"}
rate = PeriodicRate(RATE, 1)
calculation = rate.calculate(current_date=START_DATE,
                             balance=STARTING_BALANCE,
                             accrued=Decimal('0.0'))
print(calculation)

# %% [markdown] papermill={"duration": 0.001633, "end_time": "2025-08-06T12:37:03.740384", "exception": false, "start_time": "2025-08-06T12:37:03.738751", "status": "completed"}
# So collecting the daily amounts over a full year, we can see the compounded result.

# %% papermill={"duration": 0.007687, "end_time": "2025-08-06T12:37:03.749567", "exception": false, "start_time": "2025-08-06T12:37:03.741880", "status": "completed"}
state_updater = StateUpdater(rate, ANNUAL_UPDATER_PROVIDER)
final_state = reduce(lambda state, day: state_updater.update(day, state), DAYS, INITIAL_STATE)
print(final_state)

# %% papermill={"duration": 0.027897, "end_time": "2025-08-06T12:37:03.779153", "exception": false, "start_time": "2025-08-06T12:37:03.751256", "status": "completed"}
rate = PeriodicRate(RATE, 4)
calculation = rate.calculate(current_date=START_DATE,
                             balance=STARTING_BALANCE,
                             accrued=Decimal('0.0'))
print(calculation)

# %% papermill={"duration": 0.016609, "end_time": "2025-08-06T12:37:03.797417", "exception": false, "start_time": "2025-08-06T12:37:03.780808", "status": "completed"}
state_updater = StateUpdater(rate, QUARTERLY_UPDATER_PROVIDER)
final_state = reduce(lambda state, day: state_updater.update(day, state), DAYS, INITIAL_STATE)
print(final_state)

# %% [markdown] papermill={"duration": 0.001598, "end_time": "2025-08-06T12:37:03.800930", "exception": false, "start_time": "2025-08-06T12:37:03.799332", "status": "completed"}
# > **_NB._** We can see an error here as the total is slightly less than the expected 10,150.
# > This is due to an inadequacy in the algorithm. The rate calculation assumes that
# > quarters are of equal length. This is not the case and can't really be the case, as years
# > cannot be divided into a four equal number of days. We are actually using 3 calendar months
# > per quarter.
# >
# > So why is the result slightly less? This is due to compounding as payments from earlier quarters
# > compound more than those from later quarters. There are fewer days in the first
# > two quarters than the second two, but the daily rate is the same. This means that fewer days
# > of payments are compounded from the first half of the year than if the periods were equal
# > length. The fact that those days compound for more time, as the payment is earlier, does not
# > compensate for the missing days.

# %% papermill={"duration": 0.004199, "end_time": "2025-08-06T12:37:03.806662", "exception": false, "start_time": "2025-08-06T12:37:03.802463", "status": "completed"}
print('Days in first half of the year', (date(2025, 7, 1) - date(2025, 1, 1)).days)
print('Days in second half of the year', (date(2026, 1, 1) - date(2025, 7, 1)).days)


# %% [markdown] papermill={"duration": 0.001653, "end_time": "2025-08-06T12:37:03.810011", "exception": false, "start_time": "2025-08-06T12:37:03.808358", "status": "completed"}
# > **_NBB._** It may be possible to correct this algorithm, but any solution is likely to throw
# > up more problems. For instance what should we do if a period crosses between a regular year
# > and a leap year?
# >
# > For this reason it is probably unwise to use this algorithm and instead just
# > use the `ContinuousRate` in simulations as the differences are likely to be
# > insignificant.
# >
# > So why is it here? Well, when investigating how banks calculate interest. It was found that
# > this is how they say they do it. For instance: https://www.abnamro.nl/en/personal/savings/interest-rates/when-and-how-often-do-you-receive-interest.html
# >
# > However, this did not give any indication of how they compensate for unequal quarters or
# > leap years. As such, the implementation here is probably wrong anyway, so just don't use it!

# %% [markdown] papermill={"duration": 0.00162, "end_time": "2025-08-06T12:37:03.813237", "exception": false, "start_time": "2025-08-06T12:37:03.811617", "status": "completed"}
# ## BandedRate
#
# This rate combines a dictionary of rates that will be applied at different balance amounts.

# %% [markdown] papermill={"duration": 0.001566, "end_time": "2025-08-06T12:37:03.816378", "exception": false, "start_time": "2025-08-06T12:37:03.814812", "status": "completed"}
# Each call to calculate will return the daily amount associated with the given annual rate.

# %% papermill={"duration": 0.115888, "end_time": "2025-08-06T12:37:03.933877", "exception": false, "start_time": "2025-08-06T12:37:03.817989", "status": "completed"}
rate = create_banded_rate({k: ContinuousRate(v) for k, v in BANDS.items()})
calculation = rate.calculate(current_date=START_DATE,
                             balance=STARTING_BALANCE,
                             accrued=Decimal('0.0'))
print(calculation)

# %% [markdown] papermill={"duration": 0.00182, "end_time": "2025-08-06T12:37:03.937840", "exception": false, "start_time": "2025-08-06T12:37:03.936020", "status": "completed"}
# So collecting the daily amounts over a full year, we can see the compounded result.

# %% papermill={"duration": 0.022687, "end_time": "2025-08-06T12:37:03.962227", "exception": false, "start_time": "2025-08-06T12:37:03.939540", "status": "completed"}
state_updater = StateUpdater(rate, DAILY_UPDATER_PROVIDER)
final_state = reduce(lambda state, day: state_updater.update(day, state), DAYS, INITIAL_STATE)
print(final_state)

# %% papermill={"duration": 0.137324, "end_time": "2025-08-06T12:37:04.101891", "exception": false, "start_time": "2025-08-06T12:37:03.964567", "status": "completed"}
rate = create_banded_rate({k: PeriodicRate(v, 4) for k, v in BANDS.items()})
calculation = rate.calculate(current_date=START_DATE,
                             balance=STARTING_BALANCE,
                             accrued=Decimal('0.0'))
print(calculation)

# %% papermill={"duration": 0.019421, "end_time": "2025-08-06T12:37:04.123332", "exception": false, "start_time": "2025-08-06T12:37:04.103911", "status": "completed"}
state_updater = StateUpdater(rate, QUARTERLY_UPDATER_PROVIDER)
final_state = reduce(lambda state, day: state_updater.update(day, state), DAYS, INITIAL_STATE)
print(final_state)

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
# # Schedules
#
# A collection of schedule implementations that will take the current date and check if that day
# is in the schedule. The returned `Scheduled` instance will also indicate if the schedule is complete.

# %%
from calendar import TUESDAY, SATURDAY, JANUARY, FEBRUARY, APRIL, JULY, OCTOBER
from datetime import date, timedelta

from financial_simulator.schedules import \
    NeverSchedule, \
    DailySchedule, \
    DaySchedule, \
    FromSchedule, \
    UntilSchedule, \
    RangeSchedule, \
    WeeklySchedule, \
    MonthlySchedule, \
    YearlySchedule, \
    FilterSchedule, \
    AnySchedule, \
    AllSchedule, \
    Scheduled
from financial_simulator.utils.format import \
    format_day, \
    format_days

START_DATE = date.today()

print(f'Start Date: {format_day(START_DATE)}')

# %% [markdown]
# ## Primitive schedules
#
# The following schedules are the basic building blocks of schedules.

# %% [markdown]
# ### NeverSchedule
#
# This is a trivial schedule in that it always returns False

# %%
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, NeverSchedule().check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### DailySchedule
#
# This is a trivial schedule in that it always returns True

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
days_and_scheduled = [(day, DailySchedule().check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### DaySchedule
#
# This schedule will only match on the specified day

# %%
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, DaySchedule(START_DATE + timedelta(days=50)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### FromSchedule
#
# This schedule will match on all dates after and including the specified day

# %%
days = [START_DATE + timedelta(days=i) for i in range(20)]
days_and_scheduled = [(day, FromSchedule(START_DATE + timedelta(days=10)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### UntilSchedule
#
# This schedule will match on all dates up to but not including the specified day

# %%
days = [START_DATE + timedelta(days=i) for i in range(20)]
days_and_scheduled = [(day, UntilSchedule(START_DATE + timedelta(days=10)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### RangeSchedule
#
# This schedule will match on all dates after and including the `from_date` up to but not including
# the `until_date`

# %%
days = [START_DATE + timedelta(days=i) for i in range(30)]
days_and_scheduled = [(day, RangeSchedule(from_date=START_DATE + timedelta(days=10),
                                          until_date=START_DATE + timedelta(days=20)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### WeeklySchedule
#
# This schedule will match on the specified day of the week

# %%
days = [START_DATE + timedelta(days=i) for i in range(50)]
days_and_scheduled = [(day, WeeklySchedule(TUESDAY).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### MonthlySchedule
#
# This schedule will match on the specified day of the month.
#
# > **_NB._** If the current month does not have the specified day (e.g., there is no 30th of February in any year)
# then the last day of the month will match.

# %%
days = [START_DATE + timedelta(days=i) for i in range(500)]
days_and_scheduled = [(day, MonthlySchedule(30).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### YearlySchedule
#
# This schedule will match on the specified day of specified month.
#
# > **_NB._** If the current month does not have the specified day (e.g., there is no 30th of February in any year)
# then the last day of the month will match.

# %%
days = [START_DATE + timedelta(days=i) for i in range(5000)]
days_and_scheduled = [(day, YearlySchedule(FEBRUARY, 30).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### FilterSchedule
#
# This is a generic schedule that takes a callback function that will be used to check the supplied date

# %%
days = [START_DATE + timedelta(days=i) for i in range(20)]


def filter_func(current_date: date) -> Scheduled:
    return Scheduled(match=current_date.weekday() < SATURDAY,
                     complete=False)


days_and_scheduled = [(day, FilterSchedule(filter_func).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ## Schedule operators
#
# The following schedules take other schedules and apply an operator to them.

# %% [markdown]
# ### AnySchedule
#
# This represents a boolean `OR` operator for schedules. If any of the child schedules match the current date,
# then this schedule will match.
#
# For example, to get a quarterly schedule, you could create four Yearly schedules and Any them together.

# %%
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, AnySchedule((YearlySchedule(JANUARY, 1),
                                         YearlySchedule(APRIL, 1),
                                         YearlySchedule(JULY, 1),
                                         YearlySchedule(OCTOBER, 1))).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown]
# ### AllSchedule
#
# This represents a boolean `AND` operator for schedules. Only if all the child schedules match the current date,
# will this schedule match.
#
# For example, to get a weekly schedule but only until a certain date.

# %%
days = [START_DATE + timedelta(days=i) for i in range(50)]
days_and_scheduled = [(day, AllSchedule((WeeklySchedule(TUESDAY),
                                         UntilSchedule(START_DATE + timedelta(days=30)))).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

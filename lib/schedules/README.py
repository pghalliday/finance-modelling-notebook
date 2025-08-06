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

# %% [markdown] papermill={"duration": 0.00535, "end_time": "2025-08-06T12:37:09.976752", "exception": false, "start_time": "2025-08-06T12:37:09.971402", "status": "completed"}
# # Schedules
#
# A collection of schedule implementations that will take the current date and check if that day
# is in the schedule. The returned `Scheduled` instance will also indicate if the schedule is complete.

# %% papermill={"duration": 0.028015, "end_time": "2025-08-06T12:37:10.009482", "exception": false, "start_time": "2025-08-06T12:37:09.981467", "status": "completed"}
from calendar import TUESDAY, SATURDAY, JANUARY, FEBRUARY, APRIL, JULY, OCTOBER
from datetime import date, timedelta

from lib.schedules import \
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
from lib.utils.format import \
    format_day, \
    format_days

START_DATE = date.today()

print(f'Start Date: {format_day(START_DATE)}')

# %% [markdown] papermill={"duration": 0.002014, "end_time": "2025-08-06T12:37:10.013949", "exception": false, "start_time": "2025-08-06T12:37:10.011935", "status": "completed"}
# ## Primitive schedules
#
# The following schedules are the basic building blocks of schedules.

# %% [markdown] papermill={"duration": 0.002194, "end_time": "2025-08-06T12:37:10.018159", "exception": false, "start_time": "2025-08-06T12:37:10.015965", "status": "completed"}
# ### NeverSchedule
#
# This is a trivial schedule in that it always returns False

# %% papermill={"duration": 0.007965, "end_time": "2025-08-06T12:37:10.028158", "exception": false, "start_time": "2025-08-06T12:37:10.020193", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, NeverSchedule().check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001953, "end_time": "2025-08-06T12:37:10.032655", "exception": false, "start_time": "2025-08-06T12:37:10.030702", "status": "completed"}
# ### DailySchedule
#
# This is a trivial schedule in that it always returns True

# %% papermill={"duration": 0.006611, "end_time": "2025-08-06T12:37:10.041142", "exception": false, "start_time": "2025-08-06T12:37:10.034531", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
days_and_scheduled = [(day, DailySchedule().check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.002019, "end_time": "2025-08-06T12:37:10.045468", "exception": false, "start_time": "2025-08-06T12:37:10.043449", "status": "completed"}
# ### DaySchedule
#
# This schedule will only match on the specified day

# %% papermill={"duration": 0.007287, "end_time": "2025-08-06T12:37:10.054640", "exception": false, "start_time": "2025-08-06T12:37:10.047353", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, DaySchedule(START_DATE + timedelta(days=50)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001704, "end_time": "2025-08-06T12:37:10.058166", "exception": false, "start_time": "2025-08-06T12:37:10.056462", "status": "completed"}
# ### FromSchedule
#
# This schedule will match on all dates after and including the specified day

# %% papermill={"duration": 0.004964, "end_time": "2025-08-06T12:37:10.064762", "exception": false, "start_time": "2025-08-06T12:37:10.059798", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(20)]
days_and_scheduled = [(day, FromSchedule(START_DATE + timedelta(days=10)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001668, "end_time": "2025-08-06T12:37:10.068152", "exception": false, "start_time": "2025-08-06T12:37:10.066484", "status": "completed"}
# ### UntilSchedule
#
# This schedule will match on all dates up to but not including the specified day

# %% papermill={"duration": 0.004759, "end_time": "2025-08-06T12:37:10.074468", "exception": false, "start_time": "2025-08-06T12:37:10.069709", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(20)]
days_and_scheduled = [(day, UntilSchedule(START_DATE + timedelta(days=10)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001841, "end_time": "2025-08-06T12:37:10.078005", "exception": false, "start_time": "2025-08-06T12:37:10.076164", "status": "completed"}
# ### RangeSchedule
#
# This schedule will match on all dates after and including the `from_date` up to but not including
# the `until_date`

# %% papermill={"duration": 0.004775, "end_time": "2025-08-06T12:37:10.084362", "exception": false, "start_time": "2025-08-06T12:37:10.079587", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(30)]
days_and_scheduled = [(day, RangeSchedule(from_date=START_DATE + timedelta(days=10),
                                          until_date=START_DATE + timedelta(days=20)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001686, "end_time": "2025-08-06T12:37:10.087804", "exception": false, "start_time": "2025-08-06T12:37:10.086118", "status": "completed"}
# ### WeeklySchedule
#
# This schedule will match on the specified day of the week

# %% papermill={"duration": 0.004675, "end_time": "2025-08-06T12:37:10.094072", "exception": false, "start_time": "2025-08-06T12:37:10.089397", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(50)]
days_and_scheduled = [(day, WeeklySchedule(TUESDAY).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.00165, "end_time": "2025-08-06T12:37:10.097598", "exception": false, "start_time": "2025-08-06T12:37:10.095948", "status": "completed"}
# ### MonthlySchedule
#
# This schedule will match on the specified day of the month.
#
# > **_NB._** If the current month does not have the specified day (e.g., there is no 30th of February in any year)
# then the last day of the month will match.

# %% papermill={"duration": 0.005525, "end_time": "2025-08-06T12:37:10.104693", "exception": false, "start_time": "2025-08-06T12:37:10.099168", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(500)]
days_and_scheduled = [(day, MonthlySchedule(30).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001683, "end_time": "2025-08-06T12:37:10.108098", "exception": false, "start_time": "2025-08-06T12:37:10.106415", "status": "completed"}
# ### YearlySchedule
#
# This schedule will match on the specified day of specified month.
#
# > **_NB._** If the current month does not have the specified day (e.g., there is no 30th of February in any year)
# then the last day of the month will match.

# %% papermill={"duration": 0.011839, "end_time": "2025-08-06T12:37:10.121555", "exception": false, "start_time": "2025-08-06T12:37:10.109716", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(5000)]
days_and_scheduled = [(day, YearlySchedule(FEBRUARY, 30).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001808, "end_time": "2025-08-06T12:37:10.125183", "exception": false, "start_time": "2025-08-06T12:37:10.123375", "status": "completed"}
# ### FilterSchedule
#
# This is a generic schedule that takes a callback function that will be used to check the supplied date

# %% papermill={"duration": 0.004951, "end_time": "2025-08-06T12:37:10.131840", "exception": false, "start_time": "2025-08-06T12:37:10.126889", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(20)]


def filter_func(current_date: date) -> Scheduled:
    return Scheduled(match=current_date.weekday() < SATURDAY,
                     complete=False)


days_and_scheduled = [(day, FilterSchedule(filter_func).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001757, "end_time": "2025-08-06T12:37:10.135390", "exception": false, "start_time": "2025-08-06T12:37:10.133633", "status": "completed"}
# ## Schedule operators
#
# The following schedules take other schedules and apply an operator to them.

# %% [markdown] papermill={"duration": 0.001688, "end_time": "2025-08-06T12:37:10.138766", "exception": false, "start_time": "2025-08-06T12:37:10.137078", "status": "completed"}
# ### AnySchedule
#
# This represents a boolean `OR` operator for schedules. If any of the child schedules match the current date,
# then this schedule will match.
#
# For example, to get a quarterly schedule, you could create four Yearly schedules and Any them together.

# %% papermill={"duration": 0.011485, "end_time": "2025-08-06T12:37:10.151958", "exception": false, "start_time": "2025-08-06T12:37:10.140473", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, AnySchedule((YearlySchedule(JANUARY, 1),
                                         YearlySchedule(APRIL, 1),
                                         YearlySchedule(JULY, 1),
                                         YearlySchedule(OCTOBER, 1))).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

# %% [markdown] papermill={"duration": 0.001704, "end_time": "2025-08-06T12:37:10.155467", "exception": false, "start_time": "2025-08-06T12:37:10.153763", "status": "completed"}
# ### AllSchedule
#
# This represents a boolean `AND` operator for schedules. Only if all the child schedules match the current date,
# will this schedule match.
#
# For example, to get a weekly schedule but only until a certain date.

# %% papermill={"duration": 0.005252, "end_time": "2025-08-06T12:37:10.162418", "exception": false, "start_time": "2025-08-06T12:37:10.157166", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(50)]
days_and_scheduled = [(day, AllSchedule((WeeklySchedule(TUESDAY),
                                         UntilSchedule(START_DATE + timedelta(days=30)))).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')

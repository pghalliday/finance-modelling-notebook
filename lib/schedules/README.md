# Schedules

A collection of schedule implementations that will take the current date and check if that day
is in the schedule. The returned `Scheduled` instance will also indicate if the schedule is complete.


```python
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
```

    Start Date: 2025-08-06 : Wed


## Primitive schedules

The following schedules are the basic building blocks of schedules.

### NeverSchedule

This is a trivial schedule in that it always returns False


```python
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, NeverSchedule().check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    []
    Completed: 2025-08-06 : Wed


### DailySchedule

This is a trivial schedule in that it always returns True


```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
days_and_scheduled = [(day, DailySchedule().check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-06 : Wed
     2025-08-07 : Thu
     2025-08-08 : Fri
     2025-08-09 : Sat
     2025-08-10 : Sun
     2025-08-11 : Mon
     2025-08-12 : Tue
     2025-08-13 : Wed
     2025-08-14 : Thu
     2025-08-15 : Fri]
    Completed: Not completed


### DaySchedule

This schedule will only match on the specified day


```python
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, DaySchedule(START_DATE + timedelta(days=50)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-09-25 : Thu]
    Completed: 2025-09-25 : Thu


### FromSchedule

This schedule will match on all dates after and including the specified day


```python
days = [START_DATE + timedelta(days=i) for i in range(20)]
days_and_scheduled = [(day, FromSchedule(START_DATE + timedelta(days=10)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-16 : Sat
     2025-08-17 : Sun
     2025-08-18 : Mon
     2025-08-19 : Tue
     2025-08-20 : Wed
     2025-08-21 : Thu
     2025-08-22 : Fri
     2025-08-23 : Sat
     2025-08-24 : Sun
     2025-08-25 : Mon]
    Completed: Not completed


### UntilSchedule

This schedule will match on all dates up to but not including the specified day


```python
days = [START_DATE + timedelta(days=i) for i in range(20)]
days_and_scheduled = [(day, UntilSchedule(START_DATE + timedelta(days=10)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-06 : Wed
     2025-08-07 : Thu
     2025-08-08 : Fri
     2025-08-09 : Sat
     2025-08-10 : Sun
     2025-08-11 : Mon
     2025-08-12 : Tue
     2025-08-13 : Wed
     2025-08-14 : Thu
     2025-08-15 : Fri]
    Completed: 2025-08-15 : Fri


### RangeSchedule

This schedule will match on all dates after and including the `from_date` up to but not including
the `until_date`


```python
days = [START_DATE + timedelta(days=i) for i in range(30)]
days_and_scheduled = [(day, RangeSchedule(from_date=START_DATE + timedelta(days=10),
                                          until_date=START_DATE + timedelta(days=20)).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-16 : Sat
     2025-08-17 : Sun
     2025-08-18 : Mon
     2025-08-19 : Tue
     2025-08-20 : Wed
     2025-08-21 : Thu
     2025-08-22 : Fri
     2025-08-23 : Sat
     2025-08-24 : Sun
     2025-08-25 : Mon]
    Completed: 2025-08-25 : Mon


### WeeklySchedule

This schedule will match on the specified day of the week


```python
days = [START_DATE + timedelta(days=i) for i in range(50)]
days_and_scheduled = [(day, WeeklySchedule(TUESDAY).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-12 : Tue
     2025-08-19 : Tue
     2025-08-26 : Tue
     2025-09-02 : Tue
     2025-09-09 : Tue
     2025-09-16 : Tue
     2025-09-23 : Tue]
    Completed: Not completed


### MonthlySchedule

This schedule will match on the specified day of the month.

> **_NB._** If the current month does not have the specified day (e.g., there is no 30th of February in any year)
then the last day of the month will match.


```python
days = [START_DATE + timedelta(days=i) for i in range(500)]
days_and_scheduled = [(day, MonthlySchedule(30).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-30 : Sat
     2025-09-30 : Tue
     2025-10-30 : Thu
     2025-11-30 : Sun
     2025-12-30 : Tue
     2026-01-30 : Fri
     2026-02-28 : Sat
     2026-03-30 : Mon
     2026-04-30 : Thu
     2026-05-30 : Sat
     2026-06-30 : Tue
     2026-07-30 : Thu
     2026-08-30 : Sun
     2026-09-30 : Wed
     2026-10-30 : Fri
     2026-11-30 : Mon]
    Completed: Not completed


### YearlySchedule

This schedule will match on the specified day of specified month.

> **_NB._** If the current month does not have the specified day (e.g., there is no 30th of February in any year)
then the last day of the month will match.


```python
days = [START_DATE + timedelta(days=i) for i in range(5000)]
days_and_scheduled = [(day, YearlySchedule(FEBRUARY, 30).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2026-02-28 : Sat
     2027-02-28 : Sun
     2028-02-29 : Tue
     2029-02-28 : Wed
     2030-02-28 : Thu
     2031-02-28 : Fri
     2032-02-29 : Sun
     2033-02-28 : Mon
     2034-02-28 : Tue
     2035-02-28 : Wed
     2036-02-29 : Fri
     2037-02-28 : Sat
     2038-02-28 : Sun
     2039-02-28 : Mon]
    Completed: Not completed


### FilterSchedule

This is a generic schedule that takes a callback function that will be used to check the supplied date


```python
days = [START_DATE + timedelta(days=i) for i in range(20)]


def filter_func(current_date: date) -> Scheduled:
    return Scheduled(match=current_date.weekday() < SATURDAY,
                     complete=False)


days_and_scheduled = [(day, FilterSchedule(filter_func).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-06 : Wed
     2025-08-07 : Thu
     2025-08-08 : Fri
     2025-08-11 : Mon
     2025-08-12 : Tue
     2025-08-13 : Wed
     2025-08-14 : Thu
     2025-08-15 : Fri
     2025-08-18 : Mon
     2025-08-19 : Tue
     2025-08-20 : Wed
     2025-08-21 : Thu
     2025-08-22 : Fri
     2025-08-25 : Mon]
    Completed: Not completed


## Schedule operators

The following schedules take other schedules and apply an operator to them.

### AnySchedule

This represents a boolean `OR` operator for schedules. If any of the child schedules match the current date,
then this schedule will match.

For example, to get a quarterly schedule, you could create four Yearly schedules and Any them together.


```python
days = [START_DATE + timedelta(days=i) for i in range(1000)]
days_and_scheduled = [(day, AnySchedule((YearlySchedule(JANUARY, 1),
                                         YearlySchedule(APRIL, 1),
                                         YearlySchedule(JULY, 1),
                                         YearlySchedule(OCTOBER, 1))).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-10-01 : Wed
     2026-01-01 : Thu
     2026-04-01 : Wed
     2026-07-01 : Wed
     2026-10-01 : Thu
     2027-01-01 : Fri
     2027-04-01 : Thu
     2027-07-01 : Thu
     2027-10-01 : Fri
     2028-01-01 : Sat
     2028-04-01 : Sat]
    Completed: Not completed


### AllSchedule

This represents a boolean `AND` operator for schedules. Only if all the child schedules match the current date,
will this schedule match.

For example, to get a weekly schedule but only until a certain date.


```python
days = [START_DATE + timedelta(days=i) for i in range(50)]
days_and_scheduled = [(day, AllSchedule((WeeklySchedule(TUESDAY),
                                         UntilSchedule(START_DATE + timedelta(days=30)))).check(day)) for day in days]
matches = [day for day, scheduled in days_and_scheduled if scheduled.match]
completed = next((format_day(day) for day, scheduled in days_and_scheduled if scheduled.complete), 'Not completed')
print(format_days(matches))
print(f'Completed: {completed}')
```

    [2025-08-12 : Tue
     2025-08-19 : Tue
     2025-08-26 : Tue
     2025-09-02 : Tue]
    Completed: 2025-09-04 : Thu


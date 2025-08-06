# Providers

A collection of Provider implementations that will take the current date and provide sequences of values
valid for that date. The sequence will be wrapped in an instance `Provided` that will also indicate if the
provider has completed (i.e., it will not provide any more values).

```python
from calendar import TUESDAY, THURSDAY
from datetime import date, timedelta

from lib.providers import
    NeverProvider,
    AlwaysProvider,
    ScheduledProvider,
    NextProvider,
    MergeProvider,
    FunctionProvider,
    MapProvider,
    FlatMapProvider,
    MergeMapProvider,
    Provided,
    create_sequence_provider
from lib.schedules import
    WeeklySchedule,
    AnySchedule,
    UntilSchedule
from lib.utils.format import
    format_day,
    format_values

START_DATE = date.today()

print(f'Start Date: {format_day(START_DATE)}')
```

    Start Date: 2025-08-05 : Tue

## NeverProvider

This is a trivial provider that always provides an empty sequence.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(NeverProvider[str]().get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=(), complete=True)
     2025-08-06 : Wed : Provided(values=(), complete=True)
     2025-08-07 : Thu : Provided(values=(), complete=True)
     2025-08-08 : Fri : Provided(values=(), complete=True)
     2025-08-09 : Sat : Provided(values=(), complete=True)
     2025-08-10 : Sun : Provided(values=(), complete=True)
     2025-08-11 : Mon : Provided(values=(), complete=True)
     2025-08-12 : Tue : Provided(values=(), complete=True)
     2025-08-13 : Wed : Provided(values=(), complete=True)
     2025-08-14 : Thu : Provided(values=(), complete=True)]

## AlwaysProvider

This is a trivial provider that always provides a single value sequence.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(AlwaysProvider('My value').get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=('My value',), complete=False)
     2025-08-06 : Wed : Provided(values=('My value',), complete=False)
     2025-08-07 : Thu : Provided(values=('My value',), complete=False)
     2025-08-08 : Fri : Provided(values=('My value',), complete=False)
     2025-08-09 : Sat : Provided(values=('My value',), complete=False)
     2025-08-10 : Sun : Provided(values=('My value',), complete=False)
     2025-08-11 : Mon : Provided(values=('My value',), complete=False)
     2025-08-12 : Tue : Provided(values=('My value',), complete=False)
     2025-08-13 : Wed : Provided(values=('My value',), complete=False)
     2025-08-14 : Thu : Provided(values=('My value',), complete=False)]

## ScheduledProvider

This provider provides a single value sequence according to the specified schedule. If not scheduled it
provides an empty sequence.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(ScheduledProvider('My value',
                                         AnySchedule((WeeklySchedule(TUESDAY),
                                                      WeeklySchedule(THURSDAY)))).get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=('My value',), complete=False)
     2025-08-06 : Wed : Provided(values=(), complete=False)
     2025-08-07 : Thu : Provided(values=('My value',), complete=False)
     2025-08-08 : Fri : Provided(values=(), complete=False)
     2025-08-09 : Sat : Provided(values=(), complete=False)
     2025-08-10 : Sun : Provided(values=(), complete=False)
     2025-08-11 : Mon : Provided(values=(), complete=False)
     2025-08-12 : Tue : Provided(values=('My value',), complete=False)
     2025-08-13 : Wed : Provided(values=(), complete=False)
     2025-08-14 : Thu : Provided(values=('My value',), complete=False)]

## FunctionProvider

This provider uses the specified function to map the current date to an instance of `Provided`.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(FunctionProvider(lambda current_date: Provided(values=(current_date.weekday(),),
                                                                      complete=False)).get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=(1,), complete=False)
     2025-08-06 : Wed : Provided(values=(2,), complete=False)
     2025-08-07 : Thu : Provided(values=(3,), complete=False)
     2025-08-08 : Fri : Provided(values=(4,), complete=False)
     2025-08-09 : Sat : Provided(values=(5,), complete=False)
     2025-08-10 : Sun : Provided(values=(6,), complete=False)
     2025-08-11 : Mon : Provided(values=(0,), complete=False)
     2025-08-12 : Tue : Provided(values=(1,), complete=False)
     2025-08-13 : Wed : Provided(values=(2,), complete=False)
     2025-08-14 : Thu : Provided(values=(3,), complete=False)]

## NextProvider

This provider takes a sequence of providers and provides the values from the first provider that provides
a non-empty sequence of values.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(NextProvider(
    (ScheduledProvider('Value 1', UntilSchedule(START_DATE + timedelta(days=3))),
     ScheduledProvider('Value 2', UntilSchedule(START_DATE + timedelta(days=7))),
     ScheduledProvider('Value 3', UntilSchedule(START_DATE + timedelta(days=9))))).get,
                       days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=('Value 1',), complete=False)
     2025-08-06 : Wed : Provided(values=('Value 1',), complete=False)
     2025-08-07 : Thu : Provided(values=('Value 1',), complete=False)
     2025-08-08 : Fri : Provided(values=('Value 2',), complete=False)
     2025-08-09 : Sat : Provided(values=('Value 2',), complete=False)
     2025-08-10 : Sun : Provided(values=('Value 2',), complete=False)
     2025-08-11 : Mon : Provided(values=('Value 2',), complete=False)
     2025-08-12 : Tue : Provided(values=('Value 3',), complete=False)
     2025-08-13 : Wed : Provided(values=('Value 3',), complete=True)
     2025-08-14 : Thu : Provided(values=(), complete=True)]

## MergeProvider

This provider takes a sequence of providers and provides a corresponding sequence of the merged values provided
by those providers.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(MergeProvider((AlwaysProvider('Always value'),
                                      ScheduledProvider('Sometimes value', AnySchedule((WeeklySchedule(TUESDAY),
                                                                                        WeeklySchedule(THURSDAY)))),
                                      NextProvider(
                                          (ScheduledProvider('Value 1', UntilSchedule(START_DATE + timedelta(days=3))),
                                           ScheduledProvider('Value 2', UntilSchedule(START_DATE + timedelta(days=7))),
                                           ScheduledProvider('Value 3',
                                                             UntilSchedule(START_DATE + timedelta(days=9))))))).get,
                       days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=('Always value', 'Sometimes value', 'Value 1'), complete=False)
     2025-08-06 : Wed : Provided(values=('Always value', 'Value 1'), complete=False)
     2025-08-07 : Thu : Provided(values=('Always value', 'Sometimes value', 'Value 1'), complete=False)
     2025-08-08 : Fri : Provided(values=('Always value', 'Value 2'), complete=False)
     2025-08-09 : Sat : Provided(values=('Always value', 'Value 2'), complete=False)
     2025-08-10 : Sun : Provided(values=('Always value', 'Value 2'), complete=False)
     2025-08-11 : Mon : Provided(values=('Always value', 'Value 2'), complete=False)
     2025-08-12 : Tue : Provided(values=('Always value', 'Sometimes value', 'Value 3'), complete=False)
     2025-08-13 : Wed : Provided(values=('Always value', 'Value 3'), complete=False)
     2025-08-14 : Thu : Provided(values=('Always value', 'Sometimes value'), complete=False)]

## MapProvider

This provider uses the specified transform function to transform the values provided by the specified provider

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(MapProvider(transform=lambda value: (value.upper(), value.lower()),
                                   provider=ScheduledProvider(value='My value',
                                                              schedule=AnySchedule((WeeklySchedule(TUESDAY),
                                                                                    WeeklySchedule(
                                                                                        THURSDAY))))).get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=(('MY VALUE', 'my value'),), complete=False)
     2025-08-06 : Wed : Provided(values=(), complete=False)
     2025-08-07 : Thu : Provided(values=(('MY VALUE', 'my value'),), complete=False)
     2025-08-08 : Fri : Provided(values=(), complete=False)
     2025-08-09 : Sat : Provided(values=(), complete=False)
     2025-08-10 : Sun : Provided(values=(), complete=False)
     2025-08-11 : Mon : Provided(values=(), complete=False)
     2025-08-12 : Tue : Provided(values=(('MY VALUE', 'my value'),), complete=False)
     2025-08-13 : Wed : Provided(values=(), complete=False)
     2025-08-14 : Thu : Provided(values=(('MY VALUE', 'my value'),), complete=False)]

## FlatMapProvider

This provider, like the `MapProvider`, uses the specified transform function to transform the values provided
by the specified provider. However, in this case the transform function should return a sequence and these
sequences will be flattened in the resulting `Provided` instance.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(FlatMapProvider(transform=lambda value: (value.upper(), value.lower()),
                                       provider=ScheduledProvider(value='My value',
                                                                  schedule=AnySchedule((WeeklySchedule(TUESDAY),
                                                                                        WeeklySchedule(
                                                                                            THURSDAY))))).get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=('MY VALUE', 'my value'), complete=False)
     2025-08-06 : Wed : Provided(values=(), complete=False)
     2025-08-07 : Thu : Provided(values=('MY VALUE', 'my value'), complete=False)
     2025-08-08 : Fri : Provided(values=(), complete=False)
     2025-08-09 : Sat : Provided(values=(), complete=False)
     2025-08-10 : Sun : Provided(values=(), complete=False)
     2025-08-11 : Mon : Provided(values=(), complete=False)
     2025-08-12 : Tue : Provided(values=('MY VALUE', 'my value'), complete=False)
     2025-08-13 : Wed : Provided(values=(), complete=False)
     2025-08-14 : Thu : Provided(values=('MY VALUE', 'my value'), complete=False)]

## MergeMapProvider

This provider, like the `MapProvider`, uses the specified transform function to transform the values provided
by the specified provider. However, in this case, the transform function should return a new `Provider` instance.
The values from these providers will be merged in future resulting `Provided` instances.

```python
days = [START_DATE + timedelta(days=i) for i in range(15)]
sequence_days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(MergeMapProvider(
    transform=lambda current_date, value: create_sequence_provider({current_date + timedelta(days=1): f'{value}-1',
                                                                    current_date + timedelta(days=2): f'{value}-2',
                                                                    current_date + timedelta(days=3): f'{value}-3',
                                                                    current_date + timedelta(days=4): f'{value}-4'}),
    provider=create_sequence_provider({day: day.weekday() for day in sequence_days})).get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=(), complete=False)
     2025-08-06 : Wed : Provided(values=('1-1',), complete=False)
     2025-08-07 : Thu : Provided(values=('1-2', '2-1'), complete=False)
     2025-08-08 : Fri : Provided(values=('1-3', '2-2', '3-1'), complete=False)
     2025-08-09 : Sat : Provided(values=('1-4', '2-3', '3-2', '4-1'), complete=False)
     2025-08-10 : Sun : Provided(values=('2-4', '3-3', '4-2', '5-1'), complete=False)
     2025-08-11 : Mon : Provided(values=('3-4', '4-3', '5-2', '6-1'), complete=False)
     2025-08-12 : Tue : Provided(values=('4-4', '5-3', '6-2', '0-1'), complete=False)
     2025-08-13 : Wed : Provided(values=('5-4', '6-3', '0-2', '1-1'), complete=False)
     2025-08-14 : Thu : Provided(values=('6-4', '0-3', '1-2', '2-1'), complete=False)
     2025-08-15 : Fri : Provided(values=('0-4', '1-3', '2-2', '3-1'), complete=False)
     2025-08-16 : Sat : Provided(values=('1-4', '2-3', '3-2'), complete=False)
     2025-08-17 : Sun : Provided(values=('2-4', '3-3'), complete=False)
     2025-08-18 : Mon : Provided(values=('3-4',), complete=True)
     2025-08-19 : Tue : Provided(values=(), complete=True)]

## Factories

The following factory methods are available to construct combinations of providers to implement common patterns.

### create_sequence_provider

This factory takes a mapping of days to values and returns a `Provider` that will provide the given values on the
specified days.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
sequence_days = [START_DATE + timedelta(days=i) for i in range(9)]
values = zip(days, map(create_sequence_provider({day: format_day(day)
                                                 for day in sequence_days}).get, days))
print(format_values(values))
```

    [2025-08-05 : Tue : Provided(values=('2025-08-05 : Tue',), complete=False)
     2025-08-06 : Wed : Provided(values=('2025-08-06 : Wed',), complete=False)
     2025-08-07 : Thu : Provided(values=('2025-08-07 : Thu',), complete=False)
     2025-08-08 : Fri : Provided(values=('2025-08-08 : Fri',), complete=False)
     2025-08-09 : Sat : Provided(values=('2025-08-09 : Sat',), complete=False)
     2025-08-10 : Sun : Provided(values=('2025-08-10 : Sun',), complete=False)
     2025-08-11 : Mon : Provided(values=('2025-08-11 : Mon',), complete=False)
     2025-08-12 : Tue : Provided(values=('2025-08-12 : Tue',), complete=False)
     2025-08-13 : Wed : Provided(values=('2025-08-13 : Wed',), complete=True)
     2025-08-14 : Thu : Provided(values=(), complete=True)]


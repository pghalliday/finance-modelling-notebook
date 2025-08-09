<span style="color:red; font-family:Helvetica Neue, Helvetica, Arial, sans-serif; font-size:2em;">An Exception was
encountered at '<a href="#papermill-error-cell">In [10]</a>'.</span>

# Providers

A collection of Provider implementations that will take the current date and provide sequences of values
valid for that date. The sequence will be wrapped in an instance `Provided` that will also indicate if the
provider has completed (i.e., it will not provide any more values).

```python
from calendar import TUESDAY, THURSDAY
from datetime import date, timedelta

from financial_simulator.providers import \
    NeverProvider, \
    AlwaysProvider, \
    ScheduledProvider, \
    NextProvider, \
    MergeProvider, \
    FunctionProvider, \
    MapProvider, \
    FlatMapProvider, \
    MergeMapProvider, \
    Provided, \
    create_sequence_provider
from financial_simulator.schedules import \
    WeeklySchedule, \
    AnySchedule, \
    UntilSchedule
from financial_simulator.utils.format import \
    format_day, \
    format_values

START_DATE = date.today()

print(f'Start Date: {format_day(START_DATE)}')

START_DATE = date.today()

print(f'Start Date: {format_day(START_DATE)}')
```

    Start Date: 2025-08-09 : Sat
    Start Date: 2025-08-09 : Sat

## NeverProvider

This is a trivial provider that always provides an empty sequence.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(NeverProvider[str]().get, days))
print(format_values(values))
```

    [2025-08-09 : Sat : Provided(values=(), complete=True)
     2025-08-10 : Sun : Provided(values=(), complete=True)
     2025-08-11 : Mon : Provided(values=(), complete=True)
     2025-08-12 : Tue : Provided(values=(), complete=True)
     2025-08-13 : Wed : Provided(values=(), complete=True)
     2025-08-14 : Thu : Provided(values=(), complete=True)
     2025-08-15 : Fri : Provided(values=(), complete=True)
     2025-08-16 : Sat : Provided(values=(), complete=True)
     2025-08-17 : Sun : Provided(values=(), complete=True)
     2025-08-18 : Mon : Provided(values=(), complete=True)]

## AlwaysProvider

This is a trivial provider that always provides a single value sequence.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(AlwaysProvider('My value').get, days))
print(format_values(values))
```

    [2025-08-09 : Sat : Provided(values=('My value',), complete=False)
     2025-08-10 : Sun : Provided(values=('My value',), complete=False)
     2025-08-11 : Mon : Provided(values=('My value',), complete=False)
     2025-08-12 : Tue : Provided(values=('My value',), complete=False)
     2025-08-13 : Wed : Provided(values=('My value',), complete=False)
     2025-08-14 : Thu : Provided(values=('My value',), complete=False)
     2025-08-15 : Fri : Provided(values=('My value',), complete=False)
     2025-08-16 : Sat : Provided(values=('My value',), complete=False)
     2025-08-17 : Sun : Provided(values=('My value',), complete=False)
     2025-08-18 : Mon : Provided(values=('My value',), complete=False)]

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

    [2025-08-09 : Sat : Provided(values=(), complete=False)
     2025-08-10 : Sun : Provided(values=(), complete=False)
     2025-08-11 : Mon : Provided(values=(), complete=False)
     2025-08-12 : Tue : Provided(values=('My value',), complete=False)
     2025-08-13 : Wed : Provided(values=(), complete=False)
     2025-08-14 : Thu : Provided(values=('My value',), complete=False)
     2025-08-15 : Fri : Provided(values=(), complete=False)
     2025-08-16 : Sat : Provided(values=(), complete=False)
     2025-08-17 : Sun : Provided(values=(), complete=False)
     2025-08-18 : Mon : Provided(values=(), complete=False)]

## FunctionProvider

This provider uses the specified function to map the current date to an instance of `Provided`.

```python
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(FunctionProvider(lambda current_date: Provided(values=(current_date.weekday(),),
                                                                      complete=False)).get, days))
print(format_values(values))
```

    [2025-08-09 : Sat : Provided(values=(5,), complete=False)
     2025-08-10 : Sun : Provided(values=(6,), complete=False)
     2025-08-11 : Mon : Provided(values=(0,), complete=False)
     2025-08-12 : Tue : Provided(values=(1,), complete=False)
     2025-08-13 : Wed : Provided(values=(2,), complete=False)
     2025-08-14 : Thu : Provided(values=(3,), complete=False)
     2025-08-15 : Fri : Provided(values=(4,), complete=False)
     2025-08-16 : Sat : Provided(values=(5,), complete=False)
     2025-08-17 : Sun : Provided(values=(6,), complete=False)
     2025-08-18 : Mon : Provided(values=(0,), complete=False)]

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

    [2025-08-09 : Sat : Provided(values=('Value 1',), complete=False)
     2025-08-10 : Sun : Provided(values=('Value 1',), complete=False)
     2025-08-11 : Mon : Provided(values=('Value 1',), complete=False)
     2025-08-12 : Tue : Provided(values=('Value 2',), complete=False)
     2025-08-13 : Wed : Provided(values=('Value 2',), complete=False)
     2025-08-14 : Thu : Provided(values=('Value 2',), complete=False)
     2025-08-15 : Fri : Provided(values=('Value 2',), complete=False)
     2025-08-16 : Sat : Provided(values=('Value 3',), complete=False)
     2025-08-17 : Sun : Provided(values=('Value 3',), complete=True)
     2025-08-18 : Mon : Provided(values=(), complete=True)]

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

    [2025-08-09 : Sat : Provided(values=('Always value', 'Value 1'), complete=False)
     2025-08-10 : Sun : Provided(values=('Always value', 'Value 1'), complete=False)
     2025-08-11 : Mon : Provided(values=('Always value', 'Value 1'), complete=False)
     2025-08-12 : Tue : Provided(values=('Always value', 'Sometimes value', 'Value 2'), complete=False)
     2025-08-13 : Wed : Provided(values=('Always value', 'Value 2'), complete=False)
     2025-08-14 : Thu : Provided(values=('Always value', 'Sometimes value', 'Value 2'), complete=False)
     2025-08-15 : Fri : Provided(values=('Always value', 'Value 2'), complete=False)
     2025-08-16 : Sat : Provided(values=('Always value', 'Value 3'), complete=False)
     2025-08-17 : Sun : Provided(values=('Always value', 'Value 3'), complete=False)
     2025-08-18 : Mon : Provided(values=('Always value',), complete=False)]

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

    [2025-08-09 : Sat : Provided(values=(), complete=False)
     2025-08-10 : Sun : Provided(values=(), complete=False)
     2025-08-11 : Mon : Provided(values=(), complete=False)
     2025-08-12 : Tue : Provided(values=(('MY VALUE', 'my value'),), complete=False)
     2025-08-13 : Wed : Provided(values=(), complete=False)
     2025-08-14 : Thu : Provided(values=(('MY VALUE', 'my value'),), complete=False)
     2025-08-15 : Fri : Provided(values=(), complete=False)
     2025-08-16 : Sat : Provided(values=(), complete=False)
     2025-08-17 : Sun : Provided(values=(), complete=False)
     2025-08-18 : Mon : Provided(values=(), complete=False)]

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

    [2025-08-09 : Sat : Provided(values=(), complete=False)
     2025-08-10 : Sun : Provided(values=(), complete=False)
     2025-08-11 : Mon : Provided(values=(), complete=False)
     2025-08-12 : Tue : Provided(values=('MY VALUE', 'my value'), complete=False)
     2025-08-13 : Wed : Provided(values=(), complete=False)
     2025-08-14 : Thu : Provided(values=('MY VALUE', 'my value'), complete=False)
     2025-08-15 : Fri : Provided(values=(), complete=False)
     2025-08-16 : Sat : Provided(values=(), complete=False)
     2025-08-17 : Sun : Provided(values=(), complete=False)
     2025-08-18 : Mon : Provided(values=(), complete=False)]

## MergeMapProvider

This provider, like the `MapProvider`, uses the specified transform function to transform the values provided
by the specified provider. However, in this case, the transform function should return a new `Provider` instance.
The values from these providers will be merged in future resulting `Provided` instances.

<span id="papermill-error-cell" style="color:red; font-family:Helvetica Neue, Helvetica, Arial, sans-serif; font-size:2em;">
Execution using papermill encountered an exception here and stopped:</span>

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

    ---------------------------------------------------------------------------

    FrozenInstanceError                       Traceback (most recent call last)

    Cell In[10], line 9
          2 sequence_days = [START_DATE + timedelta(days=i) for i in range(10)]
          3 values = zip(days, map(MergeMapProvider(
          4     transform=lambda current_date, value: create_sequence_provider({current_date + timedelta(days=1): f'{value}-1',
          5                                                                     current_date + timedelta(days=2): f'{value}-2',
          6                                                                     current_date + timedelta(days=3): f'{value}-3',
          7                                                                     current_date + timedelta(days=4): f'{value}-4'}),
          8     provider=create_sequence_provider({day: day.weekday() for day in sequence_days})).get, days))
    ----> 9 print(format_values(values))


    File ~/projects/github/pghalliday/financial-simulator/src/financial_simulator/utils/format.py:14, in format_values(values)
         13 def format_values(values: Sequence[Tuple[date, str]]) -> str:
    ---> 14     return '[' + '\n '.join([f'{format_day(day)} : {value}' for day, value in values]) + ']'


    File ~/projects/github/pghalliday/financial-simulator/src/financial_simulator/providers/merge_map_provider.py:25, in MergeMapProvider.get(self, current_date)
         23 # for each U, transform to a new Provider
         24 sub_providers = tuple(self.transform(current_date, value) for value in provided.values)
    ---> 25 self.__sub_providers += sub_providers
         26 providers_and_provided = tuple((provider, provider.get(current_date))
         27                                for provider
         28                                in self.__sub_providers)
         29 self.__sub_providers = tuple(provider
         30                              for provider, provided in providers_and_provided
         31                              if not provided.complete)


    File <string>:17, in __setattr__(self, name, value)


    FrozenInstanceError: cannot assign to field '_MergeMapProvider__sub_providers'

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

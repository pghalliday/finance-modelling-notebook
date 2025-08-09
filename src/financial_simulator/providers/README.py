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
# # Providers
#
# A collection of Provider implementations that will take the current date and provide sequences of values
# valid for that date. The sequence will be wrapped in an instance `Provided` that will also indicate if the
# provider has completed (i.e., it will not provide any more values).

# %%
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

# %% [markdown]
# ## NeverProvider
#
# This is a trivial provider that always provides an empty sequence.

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(NeverProvider[str]().get, days))
print(format_values(values))

# %% [markdown]
# ## AlwaysProvider
#
# This is a trivial provider that always provides a single value sequence.

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(AlwaysProvider('My value').get, days))
print(format_values(values))

# %% [markdown]
# ## ScheduledProvider
#
# This provider provides a single value sequence according to the specified schedule. If not scheduled it
# provides an empty sequence.

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(ScheduledProvider('My value',
                                         AnySchedule((WeeklySchedule(TUESDAY),
                                                      WeeklySchedule(THURSDAY)))).get, days))
print(format_values(values))

# %% [markdown]
# ## FunctionProvider
#
# This provider uses the specified function to map the current date to an instance of `Provided`.

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(FunctionProvider(lambda current_date: Provided(values=(current_date.weekday(),),
                                                                      complete=False)).get, days))
print(format_values(values))

# %% [markdown]
# ## NextProvider
#
# This provider takes a sequence of providers and provides the values from the first provider that provides
# a non-empty sequence of values.

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(NextProvider(
    (ScheduledProvider('Value 1', UntilSchedule(START_DATE + timedelta(days=3))),
     ScheduledProvider('Value 2', UntilSchedule(START_DATE + timedelta(days=7))),
     ScheduledProvider('Value 3', UntilSchedule(START_DATE + timedelta(days=9))))).get,
                       days))
print(format_values(values))

# %% [markdown]
# ## MergeProvider
#
# This provider takes a sequence of providers and provides a corresponding sequence of the merged values provided
# by those providers.

# %%
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

# %% [markdown]
# ## MapProvider
#
# This provider uses the specified transform function to transform the values provided by the specified provider

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(MapProvider(transform=lambda value: (value.upper(), value.lower()),
                                   provider=ScheduledProvider(value='My value',
                                                              schedule=AnySchedule((WeeklySchedule(TUESDAY),
                                                                                    WeeklySchedule(
                                                                                        THURSDAY))))).get, days))
print(format_values(values))

# %% [markdown]
# ## FlatMapProvider
#
# This provider, like the `MapProvider`, uses the specified transform function to transform the values provided
# by the specified provider. However, in this case the transform function should return a sequence and these
# sequences will be flattened in the resulting `Provided` instance.

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(FlatMapProvider(transform=lambda value: (value.upper(), value.lower()),
                                       provider=ScheduledProvider(value='My value',
                                                                  schedule=AnySchedule((WeeklySchedule(TUESDAY),
                                                                                        WeeklySchedule(
                                                                                            THURSDAY))))).get, days))
print(format_values(values))

# %% [markdown]
# ## MergeMapProvider
#
# This provider, like the `MapProvider`, uses the specified transform function to transform the values provided
# by the specified provider. However, in this case, the transform function should return a new `Provider` instance.
# The values from these providers will be merged in future resulting `Provided` instances.

# %%
days = [START_DATE + timedelta(days=i) for i in range(15)]
sequence_days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(MergeMapProvider(
    transform=lambda current_date, value: create_sequence_provider({current_date + timedelta(days=1): f'{value}-1',
                                                                    current_date + timedelta(days=2): f'{value}-2',
                                                                    current_date + timedelta(days=3): f'{value}-3',
                                                                    current_date + timedelta(days=4): f'{value}-4'}),
    provider=create_sequence_provider({day: day.weekday() for day in sequence_days})).get, days))
print(format_values(values))

# %% [markdown]
# ## Factories
#
# The following factory methods are available to construct combinations of providers to implement common patterns.

# %% [markdown]
# ### create_sequence_provider
#
# This factory takes a mapping of days to values and returns a `Provider` that will provide the given values on the specified days.

# %%
days = [START_DATE + timedelta(days=i) for i in range(10)]
sequence_days = [START_DATE + timedelta(days=i) for i in range(9)]
values = zip(days, map(create_sequence_provider({day: format_day(day)
                                                 for day in sequence_days}).get, days))
print(format_values(values))

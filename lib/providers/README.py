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

# %% [markdown] tags=["papermill-error-cell-tag"]
# <span style="color:red; font-family:Helvetica Neue, Helvetica, Arial, sans-serif; font-size:2em;">An Exception was encountered at '<a href="#papermill-error-cell">In [10]</a>'.</span>

# %% [markdown] papermill={"duration": 0.006311, "end_time": "2025-08-06T12:37:06.114509", "exception": false, "start_time": "2025-08-06T12:37:06.108198", "status": "completed"}
# # Providers
#
# A collection of Provider implementations that will take the current date and provide sequences of values
# valid for that date. The sequence will be wrapped in an instance `Provided` that will also indicate if the
# provider has completed (i.e., it will not provide any more values).

# %% papermill={"duration": 0.018626, "end_time": "2025-08-06T12:37:06.136068", "exception": false, "start_time": "2025-08-06T12:37:06.117442", "status": "completed"}
from calendar import TUESDAY, THURSDAY
from datetime import date, timedelta

from lib.providers import \
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
from lib.schedules import \
    WeeklySchedule, \
    AnySchedule, \
    UntilSchedule
from lib.utils.format import \
    format_day, \
    format_values

START_DATE = date.today()

print(f'Start Date: {format_day(START_DATE)}')

# %% [markdown] papermill={"duration": 0.001335, "end_time": "2025-08-06T12:37:06.139080", "exception": false, "start_time": "2025-08-06T12:37:06.137745", "status": "completed"}
# ## NeverProvider
#
# This is a trivial provider that always provides an empty sequence.

# %% papermill={"duration": 0.00464, "end_time": "2025-08-06T12:37:06.145015", "exception": false, "start_time": "2025-08-06T12:37:06.140375", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(NeverProvider[str]().get, days))
print(format_values(values))

# %% [markdown] papermill={"duration": 0.00137, "end_time": "2025-08-06T12:37:06.148041", "exception": false, "start_time": "2025-08-06T12:37:06.146671", "status": "completed"}
# ## AlwaysProvider
#
# This is a trivial provider that always provides a single value sequence.

# %% papermill={"duration": 0.004496, "end_time": "2025-08-06T12:37:06.154294", "exception": false, "start_time": "2025-08-06T12:37:06.149798", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(AlwaysProvider('My value').get, days))
print(format_values(values))

# %% [markdown] papermill={"duration": 0.001396, "end_time": "2025-08-06T12:37:06.157331", "exception": false, "start_time": "2025-08-06T12:37:06.155935", "status": "completed"}
# ## ScheduledProvider
#
# This provider provides a single value sequence according to the specified schedule. If not scheduled it
# provides an empty sequence.

# %% papermill={"duration": 0.005794, "end_time": "2025-08-06T12:37:06.164508", "exception": false, "start_time": "2025-08-06T12:37:06.158714", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(ScheduledProvider('My value',
                                         AnySchedule((WeeklySchedule(TUESDAY),
                                                      WeeklySchedule(THURSDAY)))).get, days))
print(format_values(values))

# %% [markdown] papermill={"duration": 0.001572, "end_time": "2025-08-06T12:37:06.168050", "exception": false, "start_time": "2025-08-06T12:37:06.166478", "status": "completed"}
# ## FunctionProvider
#
# This provider uses the specified function to map the current date to an instance of `Provided`.

# %% papermill={"duration": 0.005806, "end_time": "2025-08-06T12:37:06.175373", "exception": false, "start_time": "2025-08-06T12:37:06.169567", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(FunctionProvider(lambda current_date: Provided(values=(current_date.weekday(),),
                                                                      complete=False)).get, days))
print(format_values(values))

# %% [markdown] papermill={"duration": 0.001594, "end_time": "2025-08-06T12:37:06.178858", "exception": false, "start_time": "2025-08-06T12:37:06.177264", "status": "completed"}
# ## NextProvider
#
# This provider takes a sequence of providers and provides the values from the first provider that provides
# a non-empty sequence of values.

# %% papermill={"duration": 0.004891, "end_time": "2025-08-06T12:37:06.185225", "exception": false, "start_time": "2025-08-06T12:37:06.180334", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(NextProvider(
    (ScheduledProvider('Value 1', UntilSchedule(START_DATE + timedelta(days=3))),
     ScheduledProvider('Value 2', UntilSchedule(START_DATE + timedelta(days=7))),
     ScheduledProvider('Value 3', UntilSchedule(START_DATE + timedelta(days=9))))).get,
                       days))
print(format_values(values))

# %% [markdown] papermill={"duration": 0.001453, "end_time": "2025-08-06T12:37:06.188324", "exception": false, "start_time": "2025-08-06T12:37:06.186871", "status": "completed"}
# ## MergeProvider
#
# This provider takes a sequence of providers and provides a corresponding sequence of the merged values provided
# by those providers.

# %% papermill={"duration": 0.005534, "end_time": "2025-08-06T12:37:06.195266", "exception": false, "start_time": "2025-08-06T12:37:06.189732", "status": "completed"}
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

# %% [markdown] papermill={"duration": 0.001773, "end_time": "2025-08-06T12:37:06.198978", "exception": false, "start_time": "2025-08-06T12:37:06.197205", "status": "completed"}
# ## MapProvider
#
# This provider uses the specified transform function to transform the values provided by the specified provider

# %% papermill={"duration": 0.005426, "end_time": "2025-08-06T12:37:06.205936", "exception": false, "start_time": "2025-08-06T12:37:06.200510", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(MapProvider(transform=lambda value: (value.upper(), value.lower()),
                                   provider=ScheduledProvider(value='My value',
                                                              schedule=AnySchedule((WeeklySchedule(TUESDAY),
                                                                                    WeeklySchedule(
                                                                                        THURSDAY))))).get, days))
print(format_values(values))

# %% [markdown] papermill={"duration": 0.00169, "end_time": "2025-08-06T12:37:06.209502", "exception": false, "start_time": "2025-08-06T12:37:06.207812", "status": "completed"}
# ## FlatMapProvider
#
# This provider, like the `MapProvider`, uses the specified transform function to transform the values provided
# by the specified provider. However, in this case the transform function should return a sequence and these
# sequences will be flattened in the resulting `Provided` instance.

# %% papermill={"duration": 0.005441, "end_time": "2025-08-06T12:37:06.217149", "exception": false, "start_time": "2025-08-06T12:37:06.211708", "status": "completed"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(FlatMapProvider(transform=lambda value: (value.upper(), value.lower()),
                                       provider=ScheduledProvider(value='My value',
                                                                  schedule=AnySchedule((WeeklySchedule(TUESDAY),
                                                                                        WeeklySchedule(
                                                                                            THURSDAY))))).get, days))
print(format_values(values))

# %% [markdown] papermill={"duration": 0.001545, "end_time": "2025-08-06T12:37:06.220485", "exception": false, "start_time": "2025-08-06T12:37:06.218940", "status": "completed"}
# ## MergeMapProvider
#
# This provider, like the `MapProvider`, uses the specified transform function to transform the values provided
# by the specified provider. However, in this case, the transform function should return a new `Provider` instance.
# The values from these providers will be merged in future resulting `Provided` instances.

# %% [markdown] tags=["papermill-error-cell-tag"]
# <span id="papermill-error-cell" style="color:red; font-family:Helvetica Neue, Helvetica, Arial, sans-serif; font-size:2em;">Execution using papermill encountered an exception here and stopped:</span>

# %% papermill={"duration": 0.229958, "end_time": "2025-08-06T12:37:06.452043", "exception": true, "start_time": "2025-08-06T12:37:06.222085", "status": "failed"}
days = [START_DATE + timedelta(days=i) for i in range(15)]
sequence_days = [START_DATE + timedelta(days=i) for i in range(10)]
values = zip(days, map(MergeMapProvider(
    transform=lambda current_date, value: create_sequence_provider({current_date + timedelta(days=1): f'{value}-1',
                                                                    current_date + timedelta(days=2): f'{value}-2',
                                                                    current_date + timedelta(days=3): f'{value}-3',
                                                                    current_date + timedelta(days=4): f'{value}-4'}),
    provider=create_sequence_provider({day: day.weekday() for day in sequence_days})).get, days))
print(format_values(values))

# %% [markdown] papermill={"duration": null, "end_time": null, "exception": null, "start_time": null, "status": "pending"}
# ## Factories
#
# The following factory methods are available to construct combinations of providers to implement common patterns.

# %% [markdown] papermill={"duration": null, "end_time": null, "exception": null, "start_time": null, "status": "pending"}
# ### create_sequence_provider
#
# This factory takes a mapping of days to values and returns a `Provider` that will provide the given values on the specified days.

# %% papermill={"duration": null, "end_time": null, "exception": null, "start_time": null, "status": "pending"}
days = [START_DATE + timedelta(days=i) for i in range(10)]
sequence_days = [START_DATE + timedelta(days=i) for i in range(9)]
values = zip(days, map(create_sequence_provider({day: format_day(day)
                                                 for day in sequence_days}).get, days))
print(format_values(values))

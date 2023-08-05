# day-nextprev


## Installation

```
$ pip install daynextprev
```

## Usage


### Calc next day

```
from daynextprev import next_day
ny, nm, nd = next_day(2015, 2, 22)
```

`datetime.date` type is supported for the argument:

```
from datetime import date
from daynextprev import next_day
the_next_day = next_day(date(2015, 5, 22))  # => datetime.date(2015, 5, 23)
```

### Calc previous day


```
from daynextprev import prev_day
py, pm, pd = prev_day(2017, 3, 1)

from datetime import date
the_prev_day = prev_day(date(2017, 3, 1))  # => datetime.date(2017, 2, 28)
```

### Iterate days

```
from daynextprev import days
for y, m, d in days((2018, 1, 1), (2018, 12, 31), include_end=True):
    print(y, m, d)

# default value for include_end is True
all_2018days = list(days((2018, 1, 1), (2018, 12, 31)))
```

You can use `datetime.date` here, too.

```
from daynextprev import days
from datetime import date
for dt_obj in days(date(2018, 1, 1), date(2018, 12, 31), include_end=True):
    print(dt_obj)
```

And you can go backward. (`days_backward` also supports `datetime.date`)

```
from daynextprev import days_backward
for y, m, d in days_backward((2018, 12, 31), (2018, 1, 1), include_end=True):
    print(y, m, d)
```


### Check leapyear

```
from daynextprev import is_leapyear
is_leapyear(2016)  # => True
```


### Calc last day of month

```
from daynextprev import days_of_month
days_of_month(2016, 2)  # => 29
```


### Calc next (year, month)

```
from daynextprev import next_month
next_y, next_m = next_month(2018, 12)  # => (2019, 1)
```

### Calc previous (year, month)

```
from daynextprev import prev_month
prev_y, prev_m = prev_month(2018, 1)  # => (2017, 12)
```

### Iterate (year, month)

```
from daynextprev import months
for year, month in months((2017, 1), (2018, 6), include_end=True):
    print(year, month)

# default value for include_end is True
all_2017months = list(months((2017, 1), (2017, 12))
```

Also you can go backward.

```
from daynextprev import months_backward
fro year, month in months((2018, 3), (2017, 10), include_end=True):
    print(year, month)

all_2017months_reversed = list(months_backward((2017, 12), (2017, 1)))
```

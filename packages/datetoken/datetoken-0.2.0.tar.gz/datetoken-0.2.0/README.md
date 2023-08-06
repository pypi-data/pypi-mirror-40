# Datetoken [![Build Status](https://travis-ci.org/sonirico/datetoken.svg?branch=master)](https://travis-ci.org/sonirico/datetoken) [![PyPI versions](https://img.shields.io/badge/python-2.7%20|%203.6-blue.svg)](https://pypi.org/project/datetoken/)

## Motivation

This package aims to solve a set of needs present in applications where
dates need to be represented in a relative fashion, like background periodic
tasks, datetime range pickers... in a compact and stringified format. This
enables the programmer to persist these tokens during the lifetime of a
process or even longer, since calculations are performed in the moment of
evaluation. Theses tokens are also useful when caching URLs as replacement
of timestamps, which would break caching given their mutability nature.

Some common examples of relative tokens:

|                                | From           | To            |
|--------------------------------|----------------|---------------|
| Today                          | `now/d`        | `now`         |
| Yesterday                      | `now-d/d`      | `now-d@d`     |
| Last 24 hours                  | `now-24h`      | `now`         |
| Last business week             | `now-w/bw`     | `now-w@bw`    |
| This business week             | `now/bw`       | `now@bw`      |
| Last month                     | `now-1M/M`     | `now-1M@M`    |
| Next week                      | `now+w/w`      | `now+w@w`     |
| Custom range                   | `now+w-2d/h`   | `now+2M-10h`  |
| Last month first business week | `now-M/M+w/bw` | `now-M/+w@bw` |

As you may have noticed, token follow a pattern:

- The word `now`. It means the point in the future timeline when tokens are
  parsed to their datetime form.
- Optionally, modifiers to add and/or subtract the future value of `now` can
  be used. Unsurprisingly, additions are set via `+`, while `-` mean
  subtractions. These modifiers can be chained as many times as needed.
  E.g: `now-1M+3d+2h`. Along with the arithmetical sign and the amount, the
  unit of time the amount refers to must be specified. Currently, the supported
  units are:
  - `s` seconds
  - `m` minutes
  - `h` hours
  - `d` days
  - `w` weeks
  - `M` months
- Optionally, there exist two extra modifiers to snap dates to the start or the
  end of any given snapshot unit. Those are:
  - `/` Snap the date to the start of the snapshot unit.
  - `@` Snap the date to the end of the snapshot unit.

  Snapshot units are the same as arithmetical modifiers, plus `bw`, meaning
  _business week_. With this, we achieve a simple way to define canonical
  relative date ranges, such as _Today_ or _Last month_. As an example of
  the later:

  - String representation: `now-1M/M`, `now-1M@M`
  - Being today _15 Jan 2018_, the result range should be:
    _2018-01-01 00:00:00 / 2018-01-31 23:59:59_


## Installing

Install and update via either [pipenv](https://pipenv.readthedocs.io/en/latest/)
or [pip](https://pip.pypa.io/en/stable/quickstart/)

```shell
pipenv install datetoken
```

or

```shell
pip install datetoken
```

## Examples

Most probably you will be dealing with simple presets such as _yesterday_ or
the _last 24 hours_.

```python
>>> from datetoken.utils import token_to_date
>>> from datetime import datetime
>>> print(datetime.utcnow())
2018-10-18 14:08:47
>>> token_to_date('now-d/d')  # Start of yesterday
2018-10-17 00:00:00
>>> token_to_date('now-d@d')  # End of yesterday
2018-10-17 23:59:59
```

However, more complex configurations are also supported so as to
provide the flexibility advanced users may need.

```python
>>> from datetoken.utils import token_to_date
>>> print(datetime.utcnow())
2018-10-18 14:34:29
>>> token_to_date('now-M+3d+100m')  # Subtract 1 month, add 3 days and
                                    # subract again 100 mintues
2018-09-21 16:14:29
```

## Issues

- Business week snapshots might not be reliable in timezones where weeks
  start in days other than Monday


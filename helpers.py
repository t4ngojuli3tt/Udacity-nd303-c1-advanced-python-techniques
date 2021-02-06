"""Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (corresponding to UTC).

The `cd_to_datetime` function converts a string, formatted as the `cd` field of
NASA's close approach data, into a Python `datetime`

The `datetime_to_str` function converts a Python `datetime` into a string.
Although `datetime`s already have human-readable string representations, those
representations display seconds, but NASA's data (and our datetimes!) don't
provide that level of resolution, so the output format also will not.
"""
import datetime


def cd_to_datetime(calendar_date):
    """Convert a NASA-formatted calendar date/time description into a datetime.

    NASA's format, at least in the `cd` field of close approach data, uses the
    English locale's month names. For example, December 31st, 2020 at noon is:

        2020-Dec-31 12:00

    This will become the Python object `datetime.datetime(2020, 12, 31, 12, 0)`.

    :param calendar_date: A calendar date in YYYY-bb-DD hh:mm format.
    :return: A naive `datetime` corresponding to the given calendar date and time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")


def datetime_to_str(dt):
    """Convert a naive Python datetime into a human-readable string.

    The default string representation of a datetime includes seconds; however,
    our data isn't that precise, so this function only formats the year, month,
    date, hour, and minute values. Additionally, this function provides the date
    in the usual ISO 8601 YYYY-MM-DD format to avoid ambiguities with
    locale-specific month names.

    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")


def default_if_empty(value, default_value, return_format=False):
    """Accept tree variable and return the first if it is not resolved to False,
       otherwise return the second. 
       The frist variable could be formated at return by third variable, by default 
       ther is no formating.

    :param value: variable to be checked if is True
    :param default_value: variable to be return if first param resolved to False
    :param return_type: optional argument, function to format value at return 
    :return: First param if it is True, second if not
    """
    if not return_format:
        return_format = type(value)
    if value:
        return return_format(value)
    else:
        return default_value


def y_to_true(x):
    """Resolved Y to True and other inputs  to False
    : param x: 
    """
    if x == "Y":
        return True
    else:
        return False

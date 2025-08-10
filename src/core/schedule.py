"""Module for scheduling date generation for content planning based on frequency and duration."""

from __future__ import annotations

from datetime import date, datetime, timedelta


def generate_dates(
    frequency: str,
    duration_weeks: int,
    start: date | None = None,
    custom_weekdays: list[int] | None = [],
) -> list[date]:
    """
    Generate a list of dates based on the given frequency and duration.

    Parameters
    ----------
    frequency : str
        Frequency of the schedule. Supported values include:
        - 'Daily': every day
        - 'Weekly': once per week on the start weekday
        - 'X times/week': custom weekdays specified by `custom_weekdays`
    duration_weeks : int
        Number of weeks to generate dates for.
    start : Optional[date], optional
        Starting date for the schedule. Defaults to today's date if None.
    custom_weekdays : list, optional
        List of integers representing weekdays (0=Monday, 6=Sunday) to use when
        frequency is 'X times/week'.
        Defaults to empty list.

    Returns
    -------
    List[date]
        List of scheduled dates.

    Examples
    --------
    >>> generate_dates('Daily', 1, date(2024, 1, 1))
    [date(2024, 1, 2), date(2024, 1, 3), ..., date(2024, 1, 8)]
    >>> generate_dates('X times/week', 2, date(2024, 1, 1), custom_weekdays=[0,2,4])
    [date(2024, 1, 1), date(2024, 1, 3), date(2024, 1, 5),
    date(2024, 1, 8), date(2024, 1, 10), date(2024, 1, 12)]
    """
    start = start or datetime.today().date()
    dates: list[date] = []

    if frequency == "Daily" or len(custom_weekdays) == 7:
        for i in range(duration_weeks * 7):
            dates.append(start + timedelta(days=i + 1))

    elif frequency == "X times/week":
        idx = sorted(set(custom_weekdays or [0, 2, 4]))
        for w in range(duration_weeks):
            base = start + timedelta(weeks=w)
            for d in idx:
                dates.append(base + timedelta(days=int(7 - start.weekday() + d)))

    else:  # Weekly
        for w in range(duration_weeks):
            dates.append(start + timedelta(weeks=w + 1, days=-start.weekday()))

    return dates


def week_index(i: int, frequency: str) -> int:
    """
    Calculate the 1-based week index for a given row index based on frequency.

    Parameters
    ----------
    i : int
        The row index (1-based).
    frequency : str
        Frequency of the schedule. Determines the number of entries per week.

    Returns
    -------
    int
        The corresponding 1-based week index.

    Examples
    --------
    >>> week_index(1, 'Daily')
    1
    >>> week_index(8, 'Daily')
    2
    >>> week_index(5, 'X times/week')
    2
    """
    denom = 7 if frequency == "Daily" else 3 if frequency in ["X times/week"] else 1
    return (i - 1) // denom + 1

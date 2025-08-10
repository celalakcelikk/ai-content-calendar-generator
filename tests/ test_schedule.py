"""Unit tests for the generate_dates function in src/core/schedule.py.

These tests validate the correct generation of dates based on different frequency inputs.
"""

from datetime import datetime

from src.core.schedule import generate_dates


def test_generate_dates_daily():
    """
    Test the generate_dates function with daily frequency.

    This test verifies that the function generates the correct number of dates
    when the frequency is set to 'Daily' over a specified duration in weeks.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    dates = generate_dates(frequency="Daily", duration_weeks=2)
    assert len(dates) == 14
    assert all(isinstance(d, datetime) for d in dates)


def test_generate_dates_weekly():
    """
    Test the generate_dates function with weekly frequency.

    This test verifies that the function generates the correct number of dates
    when the frequency is set to 'Weekly' over a specified duration in weeks.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    dates = generate_dates(frequency="Weekly", duration_weeks=3)
    assert len(dates) == 3

from datetime import datetime, timedelta

from .exceptions import MonthInvalidAPIError


def total_minutes(duration, minutes_days):
        '''
        Transform datetime in minutes and sum with minutes days.

        Args:
            duration: the datetime to use as a starting point
            minutes_days: the time in minutes

        Returns:
            total minute

            >>> total_minutes(2018-09-01 00:10:00, '00:15:00')
            25
        '''
        seconds = duration.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        total_minute = (hours*60+(minutes+minutes_days))

        return total_minute


def time_difference(time_start, time_end):
    '''
    Calculate the difference between two times on the same date.

    Args:
        time_start: the time to use as a starting point
        time_end: the time to use as an end point

    Returns:
        the difference between time_start and time_end. For example:

        >>> time_difference('15:00:00', '16:00:00')
        60
    '''

    start = datetime.strptime(str(time_start), "%H:%M:%S")
    end = datetime.strptime(str(time_end), "%H:%M:%S")
    difference = end - start
    minutes = difference.total_seconds() // 60
    return minutes


def get_previous_month(month=None, year=None):
    """
    Gets the previous month.

    Verifies that the month parameter exists or is different
    from the current. If false, return the previous month

    Parameters
    ----------
        - `month`: **str** *optional*
        - `year`: **str** *optional*

    Return
    ----------
        actual month: 8/2018
        >>> get_correct_date(8,2018)
        [7, 2018]

        >>> get_correct_date(8,2019)
        [7, 2018]

        >>> get_correct_date(7,2018)
        [7, 2018]

        >>> get_correct_date(2018)
        [7, 2018]

        >>> get_correct_date()
        [7, 2018]
    """

    date_now = datetime.now().date()
    if (month is None):
        month = date_now.month - 1

    if (year is None):
        year = date_now.year

    if ((int(month) < 1) or (int(month) > 12)):
        raise MonthInvalidAPIError()

    one_month_ago = datetime(int(year), int(month), datetime.now().day, 0, 0, 0)

    if(one_month_ago.date() >= date_now):
        one_month_ago = date_now.replace(day=1)
        one_month_ago -= timedelta(days=1)

        if (one_month_ago.year > date_now.year):
            one_month_ago = one_month_ago.replace(year=date_now.year)

    return [one_month_ago.month, one_month_ago.year]

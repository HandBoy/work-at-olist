from datetime import datetime

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
    List with month and year adjusted
            actual month: 8/2018
            get_correct_date(8,2018) return [7, 2018]
            get_correct_date(8,2019) return [7, 2018]
            get_correct_date(7,2018) return [7, 2018]
            get_correct_date(2018) return [7, 2018]
            get_correct_date() return [7, 2018]
    """

    if (month is None):
        month = datetime.now().month - 1

    if (year is None):
        year = datetime.now().year

    if ((int(month) < 1) or (int(month) > 12)):
        raise MonthInvalidAPIError()

    createdate = datetime(int(year), int(month), datetime.now().day, 0, 0, 0)
    #see reformulate if funciton existents
    if(createdate.date() >= datetime.now().date()):
        month = datetime.now().month - 1
        year = datetime.now().year
        # if current month is the first month of the year
        if month <= 0:
            month = 12
            year = createdate.year - 1

    return [month, year]
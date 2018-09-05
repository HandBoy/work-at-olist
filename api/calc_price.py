from datetime import datetime
from api.datetime_utils import (time_difference, total_minutes)
import pytz


class CalcPrice():

    def __init__(self, call_start, call_end, charge):
        '''
        Class to calculate a price of the phone call

        Args:
            call_start: **datetime** when the phone call starts
            call_end: **datetime** the when the phone call ends
            charge: **datetime** the charge for apply to precify
        '''
        self.charge = charge
        self.charge_total_hour_by_day = 0
        self.call_start_time = call_start
        self.call_end_time = call_end
        self.price = 0.0

    def calculate_price(self):
        '''
        Calculate the price of a call based on the start and end date and time

        When we have the start and end dates, we need to normalize them, to
        only take the slice of time, in minutes, referring to the standard,
        with this value is calculated the price.

        we have 12 different possibilities, the first if the connection is
        totally within the standard, the second if it is totally outside.
        After that, we can have phone calls that can be a part of the standard
        and the restoutside.

        The pattern of these possibilities are initially divided into two
        cases: if the start time is greater or less than the end-of-call time

        Args:
            time_start: the time to use as a starting a call
            time_end: the time to use as an end a call

        Returns:
            the difference between time_start and time_end. For example:

            >>> time_difference('2018-09-01 14:59:00',
                                                '2018-09-01 14:53:00)
            10.62

        '''
        minutes_standard_days = 0
        duration_standard = 0
        # check how many days the phone call lasted
        days = (self.call_end_time - self.call_start_time).days
        # we need to calculate how much time each day belongs to the standard
        self.charge_total_hour_by_day = time_difference(
                                            self.charge.standard_time_start,
                                            self.charge.standard_time_end)

        if(days > 0):
            minutes_standard_days = days * self.charge_total_hour_by_day
            # normalize date in the call by the call start

            self.call_end_time = self.call_end_time.replace(
                year=self.call_start_time.year,
                month=self.call_start_time.month,
                day=self.call_start_time.day)

        # For normalize de datas, we need to find out if the beginning of the
        # call is greater or less than the end
        if (self.is_call_start_less_or_equals_than_end()):
            self.call_start_less_than_end()
        else:
            self.call_start_bigger_than_end()

        duration_standard = self.call_end_time - self.call_start_time

        total_standard_minutes = total_minutes(duration_standard,
                                               minutes_standard_days)

        price_standard = ((self.charge.standing_time_minute
                          * total_standard_minutes)
                          + self.charge.standing_time_charge)

        return round(price_standard, 2)

    def call_start_less_than_end(self):
        '''
        Check in which pattern the call fits into.

        Normalizing the start and end of the call to pick up
        only minutes from the standard.

        Example of cases:
            Standard Start ------------------- End Standard

        Start --------- End
                Start --------- End
                            Start --------- End
                                    Start --------- End
                                                Start --------- End
                Start -------------------------------- End
        '''
        if(self.is_full_standard_time_call()):
            pass
        elif(self.is_reduced_tariff_start_less_or_equals_than_end()):
            self.call_end_time = self.call_start_time
        elif(self.call_start_time.hour < self.charge.standard_time_start.hour):
            self.call_start_time = self.call_start_time.replace(
                hour=self.charge.standard_time_start.hour,
                minute=self.charge.standard_time_start.minute,
                second=self.charge.standard_time_start.second)
            if(self.call_end_time.hour > self.charge.standard_time_end.hour):
                self.call_end_time = datetime(
                    self.call_start_time.year,
                    self.call_start_time.month,
                    self.call_start_time.day,
                    self.charge.standard_time_end.hour,
                    0, 0, tzinfo=pytz.utc)
        else:
            if(self.call_end_time.hour > self.charge.standard_time_end.hour):
                self.call_end_time = datetime(
                    self.call_start_time.year,
                    self.call_start_time.month,
                    self.call_start_time.day,
                    self.charge.standard_time_end.hour,
                    0, 0, tzinfo=pytz.utc)

    def call_start_bigger_than_end(self):
        '''
        Check in which pattern the call fits into.

        Normalizing the start and end of the call to pick up
        only minutes from the standard.

        Example of cases:
            Standard Start ------------------- End Standard

            --------- End                       Start --------- # Case 3
            ------------------ End    Start ------------------  # Case 9
            ------------------ End              Start --------- # Case 7
            --------- End             Start ------------------  # Case 8
        '''

        if(self.call_start_time.hour >= self.charge.standard_time_end.hour):
            if(self.is_reduced_tariff_start_bigger_than_end()):
                self.call_end_time = self.call_start_time
            else:
                self.call_start_time = datetime(
                    self.call_end_time.year,
                    self.call_end_time.month,
                    self.call_end_time.day,
                    self.charge.standard_time_start.hour,
                    0, 0, tzinfo=pytz.utc)
        else:
            if(self.call_end_time.hour < self.charge.standard_time_start.hour):
                self.call_end_time = datetime(
                    self.call_start_time.year,
                    self.call_start_time.month,
                    self.call_start_time.day,
                    self.charge.standard_time_end.hour, 0, 0, tzinfo=pytz.utc)
            else:
                # In this case, the call starts at a time before the end of the
                # standard and ends after the standard starts
                # We have to add these two intervals
                second_interval = (datetime(
                                    self.call_start_time.year,
                                    self.call_start_time.month,
                                    self.call_start_time.day,
                                    self.charge.standard_time_end.hour,
                                    0, 0, tzinfo=pytz.utc) 
                                   - self.call_start_time)

                self.call_start_time = (datetime(
                                        self.call_start_time .year,
                                        self.call_start_time .month,
                                        self.call_start_time .day,
                                        self.charge.standard_time_start.hour,
                                        0, 0, tzinfo=pytz.utc))

                self.call_end_time = (datetime(
                                        self.call_start_time.year,
                                        self.call_start_time.month,
                                        self.call_start_time.day,
                                        self.call_end_time.hour,
                                        0, 0, tzinfo=pytz.utc)
                                      + second_interval)

    def is_call_start_less_or_equals_than_end(self):
        if (self.call_start_time.hour <= self.call_end_time.hour):
            return True

        return False

    def is_full_standard_time_call(self):
        start = (self.call_start_time.hour
                 >= self.charge.standard_time_start.hour)
        end = (self.call_end_time.hour < self.charge.standard_time_end.hour)

        if(start and end):
            return True

        return False

    def is_reduced_tariff_start_less_or_equals_than_end(self):
        if(self.call_end_time.hour < self.charge.standard_time_start.hour):
            return True
        elif (self.call_start_time.hour >= self.charge.standard_time_end.hour):
            return True

        return False

    def is_reduced_tariff_start_bigger_than_end(self):
        if(self.call_end_time.hour < self.charge.standard_time_start.hour):
            return True

        return False

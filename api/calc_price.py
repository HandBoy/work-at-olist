from datetime import datetime


class CalcPrice():
    """

    """

    def __init__(self, call_start, call_end, charge):
        self.charge = charge
        self.charge_total_hour_by_day = 0
        self.call_start_time = call_start
        self.call_end_time = call_end
        self.price = 0.0

    def calculate_price(self, time_start, time_end):
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

            >>> time_difcalculate_priceference('2018-09-01 14:59:00',
                                                '2018-09-01 14:53:00)
            10.62

        '''
        minutes_standard_days = 0
        duration_standard = 0

        # check how many days the phone call lasted
        days = (self.call_end_time - time_start).days
        # we need to calculate how much time each day belongs to the standard
        self.charge_total_hour_by_day = self.time_difference(
                                            self.charge.standard_time_start,
                                            self.charge.standard_time_end)

        if(days > 0):
            minutes_standard_days = days * self.charge_total_hour_by_day
            # normalize date in the call by the call start
            self.call_end_time = datetime.replace(year=time_start.year,
                                        month=time_start.month,
                                        day=time_start.day)

        # For normalize de datas, we need to find out if the beginning of the
        # call is greater or less than the end
        if (self.is_call_start_less_or_equals_than_end()):
                self.call_start_less_than_end()
        else:
               self.call_start_bigger_than_end()

        duration_standard = self.call_end_time - self.call_start_time

        total_standard_minutes = self.total_minutes(duration_standard,
                                                    minutes_standard_days)

        price_standard = ((self.charge.standing_time_minute
                          * total_standard_minutes)
                          + self.charge.standing_time_charge)

        return round(price_standard, 2)

    def call_start_less_than_end(self):
        '''
        verificar em qual padrão o telefonema se enquadra. 

        Normalizando o inicio e o fim da ligação para pegar apenas os minutos do padrão
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
        elif(self.is_reduced_tariff_time_call()):
            self.call_end_time = self.call_start_time
        elif(self.call_start_time.hour < self.charge.standard_time_start.hour):
            self.call_start_time = datetime.replace(
                hour=self.charge.standard_time_start.hour,
                minute=self.charge.standard_time_start.minute,
                second=self.charge.standard_time_start.second)
            if(self.call_end_time.hour > self.charge.standard_time_end.hour):
                self.call_end_time = datetime(
                    self.call_start_time.year,
                    self.call_start_time.month,
                    self.call_start_time.day,
                    self.charge.standard_time_end.hour,
                    0, 0)
        else:
            if(self.call_end_time.hour > self.charge.standard_time_end.hour):
                self.call_end_time = datetime(
                    self.call_start_time.year,
                    self.call_start_time.month,
                    self.call_start_time.day,
                    self.charge.standard_time_end.hour,
                    0, 0)

    def call_start_bigger_than_end(self):
        '''
        verificar em qual padrão o telefonema se enquadra. 

        Normalizando o inicio e o fim da ligação para pegar apenas os minutos do padrão
            Standard Start ------------------- End Standard

            --------- End                       Start ---------
            ------------------ End    Start ------------------
            ------------------ End              Start ---------
            --------- End             Start ------------------
        '''

        if(self.call_start_time.hour >= self.charge.standard_time_end.hour):
            if(self.is_reduced_tariff_time_call(self)):
                self.call_end_time = self.call_start_time
            else:
                self.call_start_time = datetime(
                    self.call_end_time.year,
                    self.call_end_time.month,
                    self.call_end_time.day,
                    self.charge.standard_time_start.hour,
                    0, 0)
        else:
            if(self.call_end_time.hour < self.charge.standard_time_start.hour):
                self.call_end_time = datetime(
                    self.call_start_time.year,
                    self.call_start_time.month,
                    self.call_start_time.day,
                    self.charge.standard_time_end.hour, 0, 0)
            else:
                self.call_start_time = (datetime.replace(
                        hour=self.charge.standard_time_end.hour,
                        minute=self.charge.standard_time_end.minute,
                        second=self.charge.standard_time_end.second)
                      - self.call_start_time)

                self.call_end_time = self.call_end_time - datetime.replace(
                        hour=self.charge.standard_time_start.hour,
                        minute=self.charge.standard_time_start.minute,
                        second=self.charge.standard_time_start.second)

    def is_call_start_less_or_equals_than_end(self):
        if (self.call_start_time <= self.call_end_time):
            return True

        return False

    def is_full_standard_time_call(self):
        start = (self.call_start_time.hour
                 >= self.charge.standard_time_start.hour)
        end = (self.call_end_time.hour < self.charge.standard_time_end.hour)

        if(start and end):
            return True

        return False

    def is_reduced_tariff_time_call(self):
        if(self.call_end_time.hour < self.charge.standard_time_start.hour):
            return True
        elif (self.call_start_time.hour >= self.charge.standard_time_end.hour):
            return True

        return False

    def total_minutes(self, duration, minutes_days):
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

    def time_difference(self, time_start, time_end):
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

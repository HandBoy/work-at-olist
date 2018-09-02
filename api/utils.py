from datetime import datetime

import pytz

from calls.models import RatePlans

from .exceptions import MonthInvalidAPIError


def get_correct_date(month=None, year=None):
    """
    Get the previous month.

    Verify that the month parameter exists or is different
    from the current. If false, return the previous month

    Parameters
    ----------
        - `month`: **str** *optional*
            number for callers
        - `year`: **str** *optional*
            number for callers

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

    if(createdate.date() >= datetime.now().date()):
        month = datetime.now().month - 1
        year = datetime.now().year
        # if current month is the first month of the year
        if month <= 0:
            month = 12
            year = createdate.year - 1
    print([month, year])

    return [month, year]


def calculate_price(timestamp_start, timestamp_end):        
    minutes_standard_days = 0
    minutes_reduced_days = 0
    duration_standard = 0    
    duration_reduced = 0
    days = (timestamp_end - timestamp_start).days
    two_intervals = False

    rate_plans = RatePlans.objects.all()

    print("INICIO:", timestamp_start)
    print("FIM:", timestamp_end)

    #for each day a full minutes
    #
    if(days > 0):
        print("days:", days)
        minutes_standard_days = days * 16 * 60
        minutes_reduced_days = days * 8 * 60
        timestamp_end = datetime(timestamp_start.year, timestamp_start.month, 
                                 timestamp_start.day, timestamp_end.hour, 
                                 timestamp_end.minute, timestamp_end.second, 
                                 tzinfo=pytz.utc)
        print("FIM:", timestamp_end)

    for plan in rate_plans:
        tax = plan.standing_time_charge       
        d1, d2 = timestamp_start.replace(tzinfo=pytz.utc), timestamp_end.replace(tzinfo=pytz.utc)
        
        if (timestamp_start.hour <= timestamp_end.hour):
            print("timestamp_start.hour < timestamp_end.hour")
            if(timestamp_start.hour >= plan.standard_time_start.hour and
                    timestamp_end.hour < plan.standard_time_end.hour):
                print("Standard time call")
                duration_standard = timestamp_end - timestamp_start  
            elif(timestamp_end.hour < plan.standard_time_start.hour):
                print("REDUCED time call (timestamp_start.hour and timestamp_end.hour) < plan.standard_time_start.hour ")
                d2 = d1
            elif (timestamp_start.hour  >= plan.standard_time_end.hour):
                print("REDUCED time call (timestamp_start.hour and timestamp_end.hour) > plan.standard_time_end.hour ")
                d2 = d1                
            elif(timestamp_start.hour < plan.standard_time_start.hour):
                print("timestamp_start.hour < plan.standard_time_start.hour")
                d1 = datetime(timestamp_start.year,  timestamp_start.month, timestamp_start.day, plan.standard_time_start.hour, 0, 0, tzinfo=pytz.utc)                 
                if(timestamp_end.hour > plan.standard_time_end.hour):
                    d2 = datetime(timestamp_start.year, timestamp_start.month, timestamp_start.day, plan.standard_time_end.hour  , 0, 0, tzinfo=pytz.utc) 
            else:
                if(timestamp_end.hour > plan.standard_time_end.hour):
                    print("timestamp_end.hour > plan.standard_time_end.hour ")
                    d2 = datetime(timestamp_start.year, timestamp_start.month, timestamp_start.day, plan.standard_time_end.hour  , 0, 0, tzinfo=pytz.utc) 
        else:
            #TODO otimizar
            print("WWWWWW timestamp_start.hour > timestamp_end.hour")
            if(timestamp_start.hour >=  plan.standard_time_end.hour):
                print("WWWWWW timestamp_start.hour >=  plan.standard_time_end.hour")
                if(timestamp_end.hour < plan.standard_time_start.hour):
                    print("REDUCED time call (timestamp_start.hour and timestamp_end.hour) < plan.standard_time_start.hour ")
                    d2 = d1
                else:
                    print("WWWWWW ELSE timestamp_start.hour >=  plan.standard_time_end.hour")
                    d1 = datetime(timestamp_end.year,  timestamp_end.month, timestamp_end.day, plan.standard_time_start.hour, 0, 0, tzinfo=pytz.utc)     
            else:
                if(timestamp_end.hour < plan.standard_time_start.hour):
                    print("WWWWWW timestamp_end.hour < plan.standard_time_start.hour")
                    d2 = datetime(timestamp_start.year, timestamp_start.month, timestamp_start.day, plan.standard_time_end.hour  , 0, 0, tzinfo=pytz.utc)
                else:
                    print("WWWWWW  ELSE timestamp_end.hour < plan.standard_time_start.hour")
                    d1 = datetime(timestamp_start.year, timestamp_start.month, timestamp_start.day, plan.standard_time_end.hour  , 0, 0, tzinfo=pytz.utc) - timestamp_start
                    d2 = timestamp_end - datetime(timestamp_end.year, timestamp_end.month, timestamp_end.day, plan.standard_time_start.hour  , 0, 0, tzinfo=pytz.utc)
                    duration_standard = d2 + d1 
                    two_intervals = True      

        if(not two_intervals):
            duration_standard = d2 - d1
                
    total_standard_minutes = calc_total_minutes(duration_standard, minutes_standard_days)
    #total_reduced_minutes = calc_total_minutes(duration_reduced, minutes_reduced_days)
    
    price_standard = plan.standing_time_minute * total_standard_minutes + tax
    price_reduced = plan.reduced_time_minute 

    print("Duração standard a pagar: ", duration_standard)
    print("Minutos standard a pagar: ", total_standard_minutes)

    print("Duração reduced a pagar: ", duration_reduced)
    #print("Minutos reduced a pagar: ", total_reduced_minutes)
    print("tax: ", tax)
            
    print("standard R$", price_standard)
    print("reduced  R$", price_reduced)
    print("TOTAL  R$", price_standard + price_reduced)

    return round(price_standard, 2)


def calc_total_minutes(duration, minutes_days):
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    total_minute = (hours*60+(minutes+minutes_days))

    print("total_minute: ", total_minute)
    return total_minute

from datetime import timedelta
from datetime import datetime
import pytz

def get_previous_month(period):
    """
    Get the previous month.
        Args:
            date_ (Date object):
    """
    last_month_period = period.replace(day=1) - timedelta(days=1)
    month = last_month_period.month
    year = last_month_period.year

    return month, year


def calculate_price(timestamp_start, timestamp_end):        
    minutes_days = 0
    duration = 0      
    days = (timestamp_end - timestamp_start).days

    if(days>0):
        minutes_days = days * 14 * 60
        timestamp_end = datetime(timestamp_start.year, timestamp_start.month, timestamp_start.day, 22, 0, 0, tzinfo=pytz.utc)

    
    if(timestamp_start.hour >= 6 and  timestamp_end.hour < 22):
        print("Standard time call")
        duration = timestamp_end - timestamp_start         
    else:
        print("Reduced tariff time call")
        if (timestamp_start.hour < 6 and  ( timestamp_end.hour >= 6 and  timestamp_end.hour  < 22)): #4
            print("timestamp_start.hour < 6 and  ( timestamp_end.hour >= 6 and  timestamp_end.hour  < 22")
            d1 = datetime(timestamp_start.year, timestamp_start.month, timestamp_start.day, 6, 0, 0, tzinfo=pytz.utc)              
            duration =  timestamp_end - d1
        elif ((timestamp_start.hour > 6 and timestamp_start.hour < 22) and   timestamp_end.hour >= 22 ): #5
            print("(timestamp_start.hour > 6 and timestamp_start.hour < 22) and   timestamp_end.hour >= 22 ")
            d2 = datetime(timestamp_end.year, timestamp_end.month, timestamp_end.day, 22, 0, 0, tzinfo=pytz.utc)            
            duration =  d2 - timestamp_start
        elif (timestamp_start.hour < 6 and   timestamp_end.hour > 22 ):
            print("call_start.timestamp.hour < 6 and   timestamp_end.hour > 22")
            d2 = datetime(timestamp_end.year, timestamp_end.month, timestamp_end.day, 22, 0, 0, tzinfo=pytz.utc)
            d1 = datetime(timestamp_start.year, timestamp_start.month, timestamp_start.day, 6, 0, 0, tzinfo=pytz.utc)
            duration =  d2 - d1

    if type(duration) != int:
        seconds = duration.total_seconds()
    else:
        seconds = 0

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    totalminutes = (hours*60+(minutes+minutes_days))
    
    price = 0.09 * totalminutes + 0.36

    print("Duração a pagar: ", duration)
    print("Minutos a pagar: ", totalminutes)
            
    print("R$", price)

    return price
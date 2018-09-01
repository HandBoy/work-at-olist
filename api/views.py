import re

from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from calls.models import Call, CallEnd, CallStart

from .exceptions import MonthInvalidAPIError, PhoneNumberInvalidAPIError
from .serializers import (CallEndSerializer, CallSerializer,
                          CallStartSerializer, MonthBillSerializer,
                          CallAfterStartSerializer)

from .utils import calculate_price, get_correct_date

# Create your views here.


class MonthlyBillingView(APIView):
    queryset = Call.objects.all()
    
    def get(self, request, phone_number, year=None, month=None):
        # First, we need to validate if the phone number received
        # is valid
        is_valid_phone = re.compile(r'^\d{10,11}$').match(phone_number)
        # If it isn't, return a 400 BAD REQUEST response
        if not is_valid_phone:
            raise PhoneNumberInvalidAPIError()

        if(month is not None and (int(month) <= 1 or int(month) >= 12)):
            raise MonthInvalidAPIError*()

        month, year = get_correct_date(month, year)
        print(month, year)
        calls = Call.objects.filter(call_start__source=phone_number, 
                                    call_end__timestamp__month=month,
                                    call_end__timestamp__year=year)

        calls_dict = []
        
        for call in calls:
            a = {'source': call.call_start.get().source,
                 'date': call.call_start.get().timestamp.date(),
                 'time': call.call_start.get().timestamp.time(),
                 'duration': call.duration,
                 'price': call.price}            
            calls_dict.append(a)
        
        serializer = MonthBillSerializer(calls_dict, many=True)
        return Response(serializer.data)


class CalculateCallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def retrieve(self, request, pk=None):        
        call = Call.objects.get(id=pk)
        call_start = CallStart.objects.get(call_id=pk)
        call_end = CallEnd.objects.get(call_id=pk)    

        call.duration = call_end.timestamp - call_start.timestamp  
        call.price = calculate_price(call_start.timestamp, call_end.timestamp)  
        call.save()

        serializer = CallSerializer(call)
        return Response(serializer.data)


class CreateCallViewSet(APIView):
    """
    Create a phone call

    Parameters
    ----------
    - `source`: **str**
        number of who made the phone call
    - `destination`: **str**
        number for callers

            {
                "source": "84998182665",
                "destination": "8499818230"
            }

    Return
    -------
    - `call_id`: **int**
        will important for end this create call
    - `source`: **str**
        number of who made the phone call
    - `destination`: **str**
        number for callers
    - `time`: **str**
        generated at creation with the date and time of the start of the call

            {
                "call_id": 91,
                "source": "84998182665",
                "destination": "8499818230",
                "time": "2018-09-01 14:59:50.948458+00:00"
            }
    """
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            call = Call()
            call.save()
            call_start = serializer.save(call_id=call)

            serializer = CallAfterStartSerializer({
                'call_id': call.pk,
                'source': call_start.source,
                'destination': call_start.destination,
                'time': call_start.timestamp
            })

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

class EndCallViewSet(APIView):
    """
    Calculate the duration, price and ending a call

    Parameters
    ----------
    - `call_id`: **int**
        Call id to finish phone call

            {
                "call_id": 91
            }

    Return
    -------
    - `destination`: **str**
        number for callers
    - `date`: **str**
        date of phone call
    - `time`: **str**
        time of phone call
    - `duration`: **str**
        phone call duration
    - `price`: **float**
        the cost of the phone call

            {
                "destination": "84998182665",
                "date": "2018-09-01",
                "time": "14:59:50.948458",
                "duration": "1:54:26.214945",
                "price": 10.62
            }

    Raises
    ------
    KeyError
        when a key error
    OtherError
        when an other error
    """
    queryset = Call.objects.all()

    def put(self, request):
        call = get_object_or_404(self.queryset,
                                 pk=request.data["call_id"])

        end_call = CallEnd(call_id=call)
        end_call.save()    
        call_start = CallStart.objects.get(call_id=call)
        call.duration = end_call.timestamp - call_start.timestamp
        call.price = calculate_price(call_start.timestamp, end_call.timestamp)
        call.save()
        serializer = MonthBillSerializer({
                'destination': call_start.destination,
                'date': call_start.timestamp.date(),
                'time': call_start.timestamp.time(),
                'duration': call.duration,
                'price': call.price
            })
        return Response(serializer.data, status=status.HTTP_201_CREATED)
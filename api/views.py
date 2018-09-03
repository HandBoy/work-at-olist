import re

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from calls.models import Call, CallEnd, CallStart

from .exceptions import MonthInvalidAPIError, PhoneNumberInvalidAPIError
from .serializers import (
                         CallSerializer, CallStartSerializer,
                         MonthBillSerializer, CallAfterStartSerializer)

from .utils import calculate_price, get_correct_date

# Create your views here.


class MonthlyBillingView(APIView):
    """
    Get the phone calls of a month

    This method receives, by url, a phone number and optionally a year and
    a month period to calculate a bill. 
    If the year or month parameter is not passed, it assumes the last month
    last month of the same year.

    Parameters
    ----------
    - `phone_number`: **int** *required*
        number of who made the phone call
    - `year`: **str** *optional*
        number for callers
    - `month`: **str** *optional*
        number for callers


    Return
    -------
    A dict with phone calls that month or last month 
    mapping keys to the corresponding


    - `destination`: **str**
        number for callers
    - `date`: **str**
        date of phone call
    - `time`: **str**
        time of phone call
    - `duration`: **str**
        phone call duration
    - `price`: **str**
        the cost of the phone call

            GET /api/billing/84998182665/2018/07/
            [
                {
                    "destination": "84996463254",
                    "date": "2018-06-30",
                    "time": "23:35:05.470011",
                    "duration": "07h:05m:00s",
                    "price": "R$3.96"
                },
                {
                    "destination": "84996463254",
                    "date": "2018-07-28",
                    "time": "16:07:48.366749",
                    "duration": "00h:09m:15s",
                    "price": "R$1.17"
                }
            ]

    Raises
    ------
    **Invalid Phone Number**:
        HTTP 400 Bad Request.
        Phone numbers must be all digits, with 2 area code digits
        and 8 or 9 phone number digits.
    """
    queryset = Call.objects.all()

    def get(self, request, phone_number, year=None, month=None):
        # First, we need to validate if the phone number received
        # is valid
        is_valid_phone = re.compile(r'^\d{10,11}$').match(phone_number)
        # If it isn't, return a 400 BAD REQUEST response
        if not is_valid_phone:
            raise PhoneNumberInvalidAPIError()

        if(month is not None and (int(month) <= 1 or int(month) >= 12)):
            raise MonthInvalidAPIError()

        month, year = get_correct_date(month, year)
        print(month, year)
        calls = Call.objects.filter(call_start__source=phone_number,
                                    call_end__timestamp__month=month,
                                    call_end__timestamp__year=year)

        calls_dict = []

        for call in calls:
            a = {'destination': call.call_start.get().destination,
                 'date': call.call_start.get().timestamp.date(),
                 'time': call.call_start.get().timestamp.time(),
                 'duration': call.format_duration,
                 'price': call.format_price}
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

    Raises
    ------
    **Invalid Phone Number**:
        HTTP 400 Bad Request.
        Phone numbers must be all digits, with 2 area code digits
        and 8 or 9 phone number digits.

    **field is required.**
        HTTP 400 Bad Request.
        source and destination are required

    **source equals destination.**
        HTTP 400 Bad Request.
        annot create a call where source is equals as the destination.
    """
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            call = Call()
            call.save()

            try:
                call_start = serializer.save(call_id=call)
            except ValidationError as err:
                call.delete()
                return Response(data=err, status=status.HTTP_400_BAD_REQUEST)

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
     A dict mapping keys to the corresponding

    - `destination`: **str**
        number for callers
    - `date`: **str**
        date of phone call
    - `time`: **str**
        time of phone call
    - `duration`: **str**
        phone call duration
    - `price`: **str**
        the cost of the phone call

            {
                "destination": "84998182665",
                "date": "2018-09-01",
                "time": "14:59:50.94845",
                "duration": "1h54h26s",
                "price": "R$10.62"
            }

    Raises
    ------
    **Id Call Not Found**:
        HTTP 404 Not Found.
        Not found. Phone call not found in database.
    """
    queryset = Call.objects.all()

    def put(self, request):
        try:
            call_id = request.data['call_id']
        except KeyError as err:
            return Response(data='{"Error": "require field call_id"}',
                            status=status.HTTP_400_BAD_REQUEST)

        call = get_object_or_404(self.queryset, pk=call_id)

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
                'duration': call.format_duration(),
                'price': call.format_price()
            })
        return Response(serializer.data, status=status.HTTP_201_CREATED)

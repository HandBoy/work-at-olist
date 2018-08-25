from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from calls.models import Call, CallStart, CallEnd
from .serializers import CallSerializer, CallStartSerializer, CallEndSerializer, MonthBillSerializer
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from datetime import datetime
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (RetrieveModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin)
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .utils import calculate_price, get_correct_date
from rest_framework.exceptions import APIException
import re

import pytz

# Create your views here.
#month, year = get_previous_month(date.today())

class PhoneNumberInvalidAPI(APIException):
    status_code = 400
    default_detail = 'Phone Number parameter was invalid'

class MonthInvalidAPI(APIException):
    status_code = 400
    default_detail = 'Month parameter was invalid'


class MonthlyBillingView(APIView):
    queryset = Call.objects.all()
    
    def get(self, request, phone_number, year=None, month=None):
        # First, we need to validate if the phone number received
        # is valid
        is_valid_phone = re.compile(r'^\d{10,11}$').match(phone_number)
        # If it isn't, return a 400 BAD REQUEST response
        if not is_valid_phone:
            raise PhoneNumberInvalidAPI()

        if(month is not None and (int(month) <= 1 or int(month) >= 12)):
            raise MonthInvalidAPI()

        month, year = get_correct_date(month, year)
        print(month, year)
        calls = Call.objects.filter(call_start__source=phone_number, 
                                    call_end__timestamp__month=month,
                                    call_end__timestamp__year=year)

        calls_dict = []
        
        for call in calls:
            a = {'source'   : call.call_start.get().source,
                'date'      : call.call_start.get().timestamp.date(),
                'time'      : call.call_start.get().timestamp.time(),
                'duration'  : call.duration,
                'price'     : call.price}            
            calls_dict.append( a )
        
        
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


class CreateCallViewSet(viewsets.ModelViewSet):
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            call = Call()
            call.save()
            callstart = serializer.save(call_id=call)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class EndCallViewSet(viewsets.ModelViewSet):
    queryset = CallEnd.objects.all()
    serializer_class = CallEndSerializer

    def perform_create(self, serializer):
        endcall = serializer.save()       
        call = Call.objects.get(id=endcall.call_id.id)
        callstart = CallStart.objects.get(call_id=endcall.call_id.id)       
        call.duration = endcall.timestamp - callstart.timestamp 
        call.price  = calculate_price(callstart.timestamp, endcall.timestamp)
        call.save()


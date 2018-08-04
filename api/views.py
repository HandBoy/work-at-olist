from django.shortcuts import render
from rest_framework import viewsets
from calls.models import Call, CallStart, CallEnd
from .serializers import CallSerializer, CallStartSerializer, CallEndSerializer
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from datetime import datetime
import pytz

# Create your views here.
class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


class CalculateCallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def retrieve(self, request, pk=None):
        call = Call.objects.get(id=pk)
        call_start = CallStart.objects.get(call_id=pk)
        call_end = CallEnd.objects.get(call_id=pk)
        serializer = CallSerializer(call)    

        if(call_start.timestamp.hour >= 6 and  call_end.timestamp.hour < 22):
            print("Standard time call")
            duration = call_end.timestamp - call_start.timestamp 
        else:
            print("Reduced tariff time call")
            if (call_start.timestamp.hour < 6 and  ( call_end.timestamp.hour > 6 and  call_end.timestamp.hour  < 22)): #4
                print("call_start.timestamp.hour < 6 and  ( call_end.timestamp.hour > 6 and  call_end.timestamp.hour  < 22)")
                d2 = datetime(call_start.timestamp.year, call_start.timestamp.month, call_start.timestamp.day, 6, 0, 0, tzinfo=pytz.utc)              
                duration =  call_end.timestamp - d2
            elif (call_start.timestamp.hour < 22 and   call_end.timestamp.hour > 22 ): #5
                print("call_start.timestamp.hour < 22 and call_end.timestamp.hour > 22")
                d2 = datetime(call_end.timestamp.year, call_end.timestamp.month, call_end.timestamp.day, 22, 0, 0, tzinfo=pytz.utc)            
                duration =  d2 - call_start.timestamp
            elif (call_start.timestamp.hour < 6 and   call_end.timestamp.hour > 22 ):
                print("call_start.timestamp.hour < 6 and   call_end.timestamp.hour > 22")
                d2 = datetime(call_end.timestamp.year, call_end.timestamp.month, call_end.timestamp.day, 22, 0, 0, tzinfo=pytz.utc)
                d1 = datetime(call_start.timestamp.year, call_start.timestamp.month, call_start.timestamp.day, 6, 0, 0, tzinfo=pytz.utc)
                duration =  d2 - d1
            else: #
                print("hooray!")
                duration =  0        

        if type(duration) is datetime:
            seconds = duration.total_seconds()
        else:
            seconds = 0
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        totalminutes = (hours*60+minutes)

        call.duration = call_end.timestamp - call_start.timestamp
        call.price = 0.09 * totalminutes + 0.36
        
        #seconds = seconds % 60
        print(duration)
        print(call_start.timestamp)
        print(call_end.timestamp)        
        print(call.duration)
        print("R$",call.price)
        #call.save()
        #print(call.call_start.source)
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
    template = 'rest_framework/api.html'

    def perform_create(self, serializer):
        endcall = serializer.save()       
        call = Call.objects.get(id=endcall.call_id.id)
        callstart = CallStart.objects.get(call_id=endcall.call_id.id)
        duration = endcall.timestamp - callstart.timestamp
        print(callstart.timestamp)
        print(endcall.timestamp)

        print(duration)
        #print(duration.days)       

        seconds = duration.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        #seconds = seconds % 60
        
        totalminutes = (hours*60+minutes)
        print(totalminutes)
        
        then = datetime.datetime.fromtimestamp(callstart.timestamp.second)
        print(then)
        #print(duration.minute)
        if(callstart.timestamp.hour >= 6 and  callstart.timestamp.hour < 22):
            print("Standard time call")
            call.duration = duration
            call.price = 0.09 * totalminutes + 0.36
            call.save()
        else:
            print("Reduced tariff time call")
            # 22 -- 6 

            # 23 -- 10 = 2h

            # 20 -- 24 = 2h 


        #Standard time call - between 6h00 and 22h00 (excluding):

        #Reduced tariff time call - between 22h00 and 6h00 (excluding):



        
from django.shortcuts import render
from rest_framework import viewsets
from calls.models import Call, CallStart, CallEnd
from .serializers import CallSerializer, CallStartSerializer, CallEndSerializer
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework import serializers
from rest_framework.response import Response

# Create your views here.
class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


class CalculateCallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


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

        #print(duration.minute)
        if(callstart.timestamp.hour >= 6 and  callstart.timestamp.hour < 22):
            print("Standard time call")
            call.duration = duration
            call.price = 0.09 * totalminutes + 0.36
            call.save()
        else:
            print("Reduced tariff time call")
        #Standard time call - between 6h00 and 22h00 (excluding):

        #Reduced tariff time call - between 22h00 and 6h00 (excluding):



        
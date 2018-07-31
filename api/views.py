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


class CreateCallViewSet2(viewsets.ModelViewSet):
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

        
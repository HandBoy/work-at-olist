from rest_framework import serializers

from calls.models import Call, CallStart


class CallStartSerializer(serializers.ModelSerializer):
    """
    Class responsible for serializing CallStart instances
    """
    class Meta:
        model = CallStart
        fields = ('source', 'destination')


class CallSerializer(serializers.Serializer):
    """
    Class responsible for serializing Call instances
    """
    class Meta:
        model = Call
        fields = '__all__'


class MonthBillSerializer(serializers.Serializer):
    """
    Class responsible for serializing CallStart instances
    """
    destination = serializers.CharField(max_length=200)
    date = serializers.CharField(max_length=200)
    time = serializers.CharField(max_length=200)
    duration = serializers.CharField(max_length=200)
    price = serializers.CharField(max_length=10)


class CallAfterStartSerializer(serializers.Serializer):
    """
    Class responsible to serializing andreturn informations after
    create a phone call
    """
    call_id = serializers.IntegerField()
    source = serializers.CharField(max_length=200)
    destination = serializers.CharField(max_length=200)
    time = serializers.CharField(max_length=200)

from rest_framework import serializers

from calls.models import Call, CallEnd, CallStart


class CallStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStart
        fields = ('source', 'destination')


class CallEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallEnd
        fields = '__all__'


class CallSerializer(serializers.Serializer):
    class Meta:
        model = Call
        fields = '__all__'


class CallStartField(serializers.RelatedField):
    def to_representation(self, value):
        start_date = value.timestamp.date()
        start_time = value.timestamp.time()
        return 'source: %s date: %s time: %s' % (value.source, start_date, start_time)


class MonthBillSerializer(serializers.Serializer):    

    destination = serializers.CharField(max_length=200)
    date = serializers.CharField(max_length=200)
    time = serializers.CharField(max_length=200)
    duration = serializers.CharField(max_length=200)
    price = serializers.CharField(max_length=10)


class CallAfterStartSerializer(serializers.Serializer):
    call_id = serializers.IntegerField()
    source = serializers.CharField(max_length=200)
    destination = serializers.CharField(max_length=200)
    time = serializers.CharField(max_length=200)
from rest_framework import serializers
from calls.models import Call, CallStart, CallEnd

class CallStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStart
        fields = ('source', 'timestamp')



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
    source = serializers.CharField(max_length=200)
    date = serializers.CharField(max_length=200)
    time = serializers.CharField(max_length=200)
    duration = serializers.CharField(max_length=200)
    price = serializers.FloatField()

    #call_start = CallStartField(many=True, read_only=True)
    #class Meta:
    #     model = Call
    #    fields = ('call_start', 'duration', 'price')


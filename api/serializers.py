from rest_framework import serializers
from calls.models import Call, CallStart, CallEnd

class CallStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStart
        fields = ('source', 'destination')


class CallEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallEnd
        fields = '__all__'


class CallSerializer(serializers.Serializer):
    start   = CallStartSerializer()
    end     = CallEndSerializer()

    class Meta:
        model = Call
        fields = '__all__'



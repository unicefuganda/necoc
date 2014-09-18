from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import fields
from dms.models.rapid_pro_message import RapidProMessage


class RapidProMessageSerializer(serializers.MongoEngineModelSerializer):
    phone = fields.CharField(source='phone_no')
    time = fields.DateTimeField(source='received_at')
    relayer = fields.IntegerField(source='relayer_id')
    sms = fields.IntegerField(source='sms_id')

    class Meta:
        model = RapidProMessage
        fields = ('phone', 'time', 'relayer', 'sms', 'text', 'relayer_phone', 'status', 'direction', 'event')


class RapidProListCreateView(ListCreateAPIView):
    serializer_class = RapidProMessageSerializer
    queryset = RapidProMessage.objects.all()
    model = RapidProMessage
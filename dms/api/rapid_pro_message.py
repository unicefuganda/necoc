from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
from dms.models.rapid_pro_message import RapidProMessage


class RapidProMessageSerializer(serializers.MongoEngineModelSerializer):
    phone = fields.CharField(source='phone_no')
    time = fields.DateTimeField(source='received_at')
    relayer = fields.IntegerField(source='relayer_id')
    sms = fields.IntegerField(source='sms_id')
    source = serialiserzz.Field(source='source')

    class Meta:
        model = RapidProMessage
        fields = ('phone', 'time', 'relayer', 'sms', 'text', 'relayer_phone', 'status', 'direction', 'event', 'source')


class RapidProListCreateView(ListCreateAPIView):
    serializer_class = RapidProMessageSerializer
    queryset = RapidProMessage.objects.all()
    model = RapidProMessage
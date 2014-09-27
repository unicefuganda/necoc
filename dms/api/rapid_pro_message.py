from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
from dms.models.rapid_pro_message import RapidProMessage


class RapidProMessageSerializer(serializers.MongoEngineModelSerializer):
    phone = fields.CharField(source='phone_no')
    time = fields.DateTimeField(source='received_at')
    relayer = fields.IntegerField(source='relayer_id')
    run = fields.IntegerField(source='run_id')
    source = serialiserzz.Field(source='source')
    location = serialiserzz.Field(source='location_str')

    class Meta:
        model = RapidProMessage
        fields = ('phone', 'time', 'relayer', 'run', 'text', 'source', 'location')


class RapidProListCreateView(ListCreateAPIView):
    serializer_class = RapidProMessageSerializer
    queryset = RapidProMessage.objects.all()
    model = RapidProMessage
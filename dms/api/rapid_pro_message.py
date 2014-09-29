from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
from dms.models import MobileUser, Location
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
    model = RapidProMessage

    def get_queryset(self):
        location_queried = self.request.GET.get('location', None)
        if location_queried:
            return self._messages_from(location_queried)
        return RapidProMessage.objects()

    def _messages_from(self, location):
        locations = list(Location.objects(parent=location))
        locations.insert(0, location)
        phone_numbers_filtered = MobileUser.objects(location__in=locations).values_list('phone')
        return RapidProMessage.objects(phone_no__in=phone_numbers_filtered)

from django.utils.datetime_safe import datetime
from django.utils.timezone import localtime
import pytz
from rest_framework.permissions import AllowAny
from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
import time
from dms.api.bulk_sms_endpoint import SentMessageListCreateView

from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models import Location, RapidProMessage, Disaster, DisasterType, AdminSetting
from dms.utils.internal_api_calls_utils import post_to_api
from necoc import settings

RAPID_PRO_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


class RapidProDateTimeField(fields.DateTimeField):
    def to_native(self, obj):
        if obj and not type(obj) is unicode:
            return localtime(obj.replace(tzinfo=pytz.utc), pytz.timezone(settings.TIME_ZONE))
        return obj

    def from_native(self, data):
        try:
            parts = data.split('.')
            time_sans_microseconds = parts[0]
            return datetime.strptime(time_sans_microseconds, RAPID_PRO_TIME_FORMAT)
        except:
            return super(fields.DateTimeField, self).from_native(data)


class RapidProMessageSerializer(serializers.MongoEngineModelSerializer):
    phone = fields.CharField(source='phone_no')
    time = RapidProDateTimeField(source='received_at')
    relayer = fields.IntegerField(source='relayer_id')
    run = fields.IntegerField(source='run_id')
    source = serialiserzz.Field(source='source')
    location = serialiserzz.Field(source='location_str')

    class Meta:
        model = RapidProMessage
        fields = ('id', 'phone', 'time', 'relayer', 'run', 'text', 'source', 'location', 'disaster')


class RapidProListCreateView(ListCreateAPIView):
    serializer_class = RapidProMessageSerializer
    permission_classes = (AllowAny,)
    model = RapidProMessage

    def get_queryset(self):
        queryset = self._non_location_queried_messages()
        location_queried = self.request.GET.get('location', None)

        if location_queried:
            location = Location.objects(id=location_queried).first()
            queryset = RapidProMessage.from_(location, _queryset=queryset)

        disaster_type = self.request.GET.get('disaster_type', None)
        if disaster_type:
            queryset = self.query_by_disaster_type(disaster_type, queryset)

        return queryset.order_by('-received_at')

    def _get_param_conversion(self, fields):
        converted = {field: field for field in fields}
        converted['to'] = 'received_at__lte'
        converted['from'] = 'received_at__gte'
        converted.pop('location', None)
        converted.pop('disaster_type', None)
        return converted

    def _non_location_queried_messages(self):
        fields = RapidProMessage.get_fields()
        converted_params = self._get_param_conversion(fields)
        query_params = {converted_params[key]: value or None for key, value in self.request.GET.items() if key in converted_params}
        return RapidProMessage.objects(**query_params)

    def query_by_disaster_type(self, disaster_type, queryset=None):
        disaster_type = DisasterType.objects(id=disaster_type).first()
        disasters = Disaster.objects(name=disaster_type)
        return queryset.filter(disaster__in=disasters)


class RapidProRetrieveUpdateView(MongoRetrieveUpdateView):
    serializer_class = RapidProMessageSerializer
    queryset = RapidProMessage.objects.all()

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

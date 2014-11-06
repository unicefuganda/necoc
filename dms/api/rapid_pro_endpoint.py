from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz

from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models import Location, RapidProMessage, Disaster, DisasterType


class RapidProMessageSerializer(serializers.MongoEngineModelSerializer):
    phone = fields.CharField(source='phone_no')
    time = fields.DateTimeField(source='received_at')
    relayer = fields.IntegerField(source='relayer_id')
    run = fields.IntegerField(source='run_id')
    source = serialiserzz.Field(source='source')
    location = serialiserzz.Field(source='location_str')

    class Meta:
        model = RapidProMessage
        fields = ('id', 'phone', 'time', 'relayer', 'run', 'text', 'source', 'location', 'disaster')


class RapidProListCreateView(ListCreateAPIView):
    serializer_class = RapidProMessageSerializer
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

        return queryset

    def _get_param_conversion(self, fields):
        converted = {field: field for field in fields}
        converted['to'] = 'received_at__lte'
        converted['from'] = 'received_at__gte'
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
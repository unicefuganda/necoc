from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz

from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models import Location, RapidProMessage


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
            queryset = RapidProMessage.from_(location, queryset)
        return queryset

    def _non_location_queried_messages(self):
        fields = RapidProMessage._fields_ordered
        query_params = {key: value or None for key, value in self.request.GET.items() if key in fields}
        return RapidProMessage.objects(**query_params)


class RapidProRetrieveUpdateView(MongoRetrieveUpdateView):
    serializer_class = RapidProMessageSerializer
    queryset = RapidProMessage.objects.all()

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)



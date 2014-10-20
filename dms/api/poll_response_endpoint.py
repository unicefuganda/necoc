from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
from rest_framework_mongoengine.generics import ListCreateAPIView

from dms.models import PollResponse, Location


class PollResponseSerializer(serializers.MongoEngineModelSerializer):
    phone = fields.CharField(source='phone_no')
    time = fields.DateTimeField(source='received_at')
    relayer = fields.IntegerField(source='relayer_id')
    run = fields.IntegerField(source='run_id')
    source = serialiserzz.Field(source='source')
    location = serialiserzz.Field(source='location_str')

    class Meta:
        model = PollResponse
        fields = ('id', 'phone', 'time', 'relayer', 'run', 'text', 'source', 'location', 'poll')


class PollResponseListCreateView(ListCreateAPIView):
    serializer_class = PollResponseSerializer
    model = PollResponse

    def get_queryset(self):
        fields = PollResponse._fields_ordered
        query_params = {key: value or None for key, value in self.request.GET.items() if key in fields}
        return PollResponse.objects(**query_params)

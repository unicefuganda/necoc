from rest_framework.permissions import AllowAny
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_csv import renderers as r
from rest_framework.settings import api_settings

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
    permission_classes = (AllowAny,)
    model = PollResponse

    def get_queryset(self):
        if self.request.DATA.get('not_assigned'):
            return PollResponse.objects(**dict(poll=None)).order_by('-created_at')
        else:
            fields = PollResponse._fields_ordered
            query_params = {key: value or None for key, value in self.request.GET.items() if key in fields}
            return PollResponse.objects(**query_params).order_by('-created_at')

class CSVPollResponseSerializer(serializers.MongoEngineModelSerializer):
    phone = fields.CharField(source='phone_no')
    time = fields.DateTimeField(source='received_at')
    source = serialiserzz.Field(source='source')
    location = serialiserzz.Field(source='location_str')
    poll_name = serialiserzz.Field(source='poll_name')

    class Meta:
        model = PollResponse
        fields = ('source', 'phone', 'text', 'time', 'location', 'poll_name')


class CSVPollResponsesView(ListCreateAPIView):
    serializer_class = CSVPollResponseSerializer
    permission_classes = (AllowAny,)
    model = PollResponse
    renderer_classes = [r.CSVRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES

    def get_queryset(self):
        params = self._filter_params(self.request)
        queryset = PollResponse.objects.filter(**params)
        return queryset.order_by('-received_at')

    def _filter_params(self, req):
        fields = PollResponse._fields_ordered
        return {key: value or None for key, value in req.GET.items() if key in fields}

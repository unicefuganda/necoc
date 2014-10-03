from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models import DisasterType
from dms.tasks import send_bulk_sms


class DisasterTypeSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = DisasterType
        exclude = ('created_at',)


class DisasterTypeListCreateView(ListCreateAPIView):
    model = DisasterType
    serializer_class = DisasterTypeSerializer
    queryset = DisasterType.objects()

    def post_save(self, obj, created=True):
        send_bulk_sms.delay(obj)
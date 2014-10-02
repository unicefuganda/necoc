from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models import SentMessage
from dms.tasks import send_bulk_sms


class SentMessageSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = SentMessage
        exclude = ('created_at',)


class SentMessageListCreateView(ListCreateAPIView):
    model = SentMessage
    serializer_class = SentMessageSerializer
    queryset = SentMessage.objects()

    def post_save(self, obj, created=True):
        send_bulk_sms.delay(obj)
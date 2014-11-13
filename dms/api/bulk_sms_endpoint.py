from rest_condition import Or
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models import SentMessage
from dms.tasks import send_bulk_sms
from dms.utils.permission_class_factory import build_permission_class, IsGetRequest


class SentMessageSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = SentMessage
        exclude = ('created_at', 'log')


class SentMessageListCreateView(ListCreateAPIView):
    model = SentMessage
    serializer_class = SentMessageSerializer
    queryset = SentMessage.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_messages'), IsGetRequest)]

    def post_save(self, obj, created=True):
        send_bulk_sms.delay(obj)
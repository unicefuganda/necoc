from rest_condition import Or
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models.response_message import ResponseMessage
from dms.tasks import send_bulk_sms
from dms.utils.permission_class_factory import build_permission_class, IsGetRequest


class ResponseMessageSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = ResponseMessage
        exclude = ('created_at', 'log')


class ResponseMessageListCreateView(ListCreateAPIView):
    model = ResponseMessage
    serializer_class = ResponseMessageSerializer
    queryset = ResponseMessage.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_messages'), IsGetRequest)]

    def post_save(self, obj, created=True):
        send_bulk_sms.delay(obj)
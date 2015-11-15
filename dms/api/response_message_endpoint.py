from rest_condition import Or
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models.response_message import ResponseMessage
from dms.tasks import send_one_sms
from dms.utils.permission_class_factory import build_permission_class, IsGetRequest
from necoc import settings


class ResponseMessageSerializer(serializers.MongoEngineModelSerializer):
    response_to = serializers.fields.CharField(source='response_to', required=False)

    class Meta:
        model = ResponseMessage
        exclude = ('created_at', 'log')


class ResponseMessageListCreateView(ListCreateAPIView):
    model = ResponseMessage
    serializer_class = ResponseMessageSerializer
    queryset = ResponseMessage.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_messages'), IsGetRequest)]

    def pre_save(self, obj):
        in_response_to = self.request.DATA.get('text', '')
        obj.text = settings.AUTO_RESPONSE_MESSAGE
        obj.response_to = in_response_to

    def post_save(self, obj, created=True):
        send_one_sms.delay(obj)
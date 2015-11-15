from rest_condition import Or
from rest_framework import fields
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models import RapidProMessage
from dms.models.response_message import ResponseMessage
from dms.tasks import send_one_sms
from dms.utils.permission_class_factory import build_permission_class, IsGetRequest
from necoc import settings


auto_response_text = settings.AUTO_RESPONSE_MESSAGE

class ResponseMessageSerializer(serializers.MongoEngineModelSerializer):

    def pre_save(self, obj):
        self.request.DATA['text'] = settings.AUTO_RESPONSE_MESSAGE
        phone_no = self.request.DATA.get('phone', None)
        if not phone_no is None:
            self.request.DATA['response_to'] = \
                RapidProMessage.objects.filter(phone_no=phone_no).order_by('-created_at').first()

    class Meta:
        model = ResponseMessage
        exclude = ('created_at', 'log')


class ResponseMessageListCreateView(ListCreateAPIView):
    model = ResponseMessage
    serializer_class = ResponseMessageSerializer
    queryset = ResponseMessage.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_messages'), IsGetRequest)]

    def post_save(self, obj, created=True):
        send_one_sms.delay(obj)
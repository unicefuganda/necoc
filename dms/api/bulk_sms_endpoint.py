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
    ordering_fields = '__all__'
    ordering = ('-created_at',)

    def get_queryset(self):
        query_params = {key: value or None for key, value in self.request.GET.items()}
        if 'ordering' in query_params:
            ordering_params = query_params['ordering']
            del query_params['ordering']
            query_set = SentMessage.objects(**query_params).order_by('%s' % ordering_params)
        else:
            query_set = SentMessage.objects(**query_params).order_by('-created_at')
        return query_set

    def post_save(self, obj, created=True):
        send_bulk_sms.delay(obj)
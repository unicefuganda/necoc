import json
import requests
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models import SentMessage
from necoc.settings import API_TOKEN, API_URL


class SentMessageSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = SentMessage
        exclude = ('created_at',)


class SentMessageListCreateView(ListCreateAPIView):
    model = SentMessage
    serializer_class = SentMessageSerializer
    queryset = SentMessage.objects()

    def pre_save(self, obj):
        data = dict(phone=obj.phone_numbers, text=obj.text)
        headers = {'Authorization': 'Token ' + API_TOKEN,
                   'content-type': 'application/json'}
        try:
            requests.post(API_URL, data=json.dumps(data), headers=headers)
        except Exception:
            pass
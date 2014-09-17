from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine.serializers import MongoEngineModelSerializer
from dms.models.rapid_pro_message import RapidProMessage


class RapidProMessageSerializer(MongoEngineModelSerializer):
    class Meta:
        model = RapidProMessage
        exclude = ('created_at', )


class RapidProListCreateView(ListCreateAPIView):
    serializer_class = RapidProMessageSerializer
    queryset = RapidProMessage.objects.all()
    model = RapidProMessage
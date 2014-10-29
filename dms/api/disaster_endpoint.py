from rest_framework import fields

from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView

from dms.models.disaster import Disaster


class DisasterSerializer(serializers.MongoEngineModelSerializer):
    status = fields.ChoiceField(source='status', choices=Disaster.DISASTER_STATUS)

    class Meta:
        model = Disaster
        depth = 4
        exclude = ('created_at',)


class DisasterListCreateView(ListCreateAPIView):
    model = Disaster
    serializer_class = DisasterSerializer
    queryset = Disaster.objects()

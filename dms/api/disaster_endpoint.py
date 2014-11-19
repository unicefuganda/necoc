from rest_condition import Or
from rest_framework import fields

from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView

from dms.models.disaster import Disaster
from dms.utils.permission_class_factory import IsGetRequest, build_permission_class


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
    permission_classes = [Or(build_permission_class('dms.can_manage_disasters'), IsGetRequest)]


class DisasterView(MongoRetrieveUpdateView):
    model = Disaster
    serializer_class = DisasterSerializer
    queryset = Disaster.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_disasters'), IsGetRequest)]

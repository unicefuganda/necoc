from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models import DisasterType
from rest_framework import serializers as rest_serializers


class DisasterTypeSerializer(serializers.MongoEngineModelSerializer):

    def validate_name(self, attrs, source):
        if len(DisasterType.objects(name=attrs[source])):
            raise rest_serializers.ValidationError('Disaster type must be unique')
        return attrs

    class Meta:
        model = DisasterType
        exclude = ('created_at',)


class DisasterTypeListCreateView(ListCreateAPIView):
    model = DisasterType
    serializer_class = DisasterTypeSerializer
    queryset = DisasterType.objects()
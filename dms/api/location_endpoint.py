from rest_framework_mongoengine.generics import ListCreateAPIView, ListAPIView
from rest_framework_mongoengine import serializers
from dms.models.location import Location


class LocationSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Location
        exclude = ('created_at',)


class LocationListCreateView(ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects()
    model = Location
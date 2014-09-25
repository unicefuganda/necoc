from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from dms.models.location import Location


class LocationSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Location
        exclude = ('created_at',)


class LocationListCreateView(ListCreateAPIView):
    model = Location
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = Location.objects()
        location_type = self.request.QUERY_PARAMS.get('type', None)
        if location_type is not None:
            queryset = Location.objects(type=location_type)
        return queryset

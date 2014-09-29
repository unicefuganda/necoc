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
        fields = Location._fields_ordered
        query_params = {key: value or None for key, value in self.request.GET.items() if key in fields}
        return Location.objects(**query_params)

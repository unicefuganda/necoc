from rest_framework import fields
from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from dms.models.location import Location


class LocationSerializer(serializers.MongoEngineModelSerializer):

    type = fields.ChoiceField(source='type', choices=Location.TYPE_CHOICES)

    class Meta:
        model = Location
        exclude = ('created_at',)


class LocationListCreateView(ListCreateAPIView):
    model = Location
    serializer_class = LocationSerializer

    def get_queryset(self):
        query_set = self.get_non_children_queryset()
        return self.get_location_children_by_type(query_set)

    def get_non_children_queryset(self):
        fields = Location._fields_ordered
        query_params = {key: value or None for key, value in self.request.GET.items() if key in fields}
        return Location.objects(**query_params)

    def get_location_children_by_type(self, query_set):
        location_types = [_type[0] for _type in Location.TYPE_CHOICES]
        parent_key = filter(lambda field: field in location_types, self.request.GET.keys())
        if parent_key:
            return query_set.filter(parent=self.request.GET.get(parent_key[0]))
        return query_set
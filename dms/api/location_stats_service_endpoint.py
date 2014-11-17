from rest_framework import serializers
from rest_framework_mongoengine.generics import ListAPIView
from rest_framework.response import Response

from dms.services.location_stats import MultiLocationStatsService


class StatsDetailsSerializer(serializers.Serializer):

    count = serializers.Field()
    percentage = serializers.Field()


class DisasterStatsDetailsSerializer(StatsDetailsSerializer):

    affected = serializers.Field()
    types = serializers.Field()


class LocationStatsSerializer(serializers.Serializer):

    messages = StatsDetailsSerializer(many=False)
    disasters = DisasterStatsDetailsSerializer(many=False)


class MultiLocationStatsSerializer(object):

    def __init__(self, location, **kwargs):
        self.stats = MultiLocationStatsService(location, **kwargs).stats()
        self.data = self._serialized_data()

    def _serialized_data(self):
        return {location_name.lower(): LocationStatsSerializer(self.stats[location_name]).data for location_name in self.stats.keys()}


class LocationStatsListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        serializer = MultiLocationStatsSerializer(None, **request.GET.dict())
        return Response(serializer.data)


class DistrictStatsListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        location = kwargs.get('district', None)
        serializer = MultiLocationStatsSerializer(location, **request.GET.dict())
        return Response(serializer.data)

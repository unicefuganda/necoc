from rest_framework import serializers
from rest_framework_mongoengine.generics import ListAPIView
from rest_framework.response import Response

from dms.services.location_stats import MultiLocationStatsService


class StatsDetailsSerializer(serializers.Serializer):

    count = serializers.Field()
    percentage = serializers.Field()


class LocationStatsSerializer(serializers.Serializer):

    messages = StatsDetailsSerializer(many=False)


class MultiLocationStatsSerializer(object):

    def __init__(self):
        self.stats = MultiLocationStatsService().stats()
        self.data = self._serialized_data()

    def _serialized_data(self):
        return {location_name: LocationStatsSerializer(self.stats[location_name]).data for location_name in self.stats.keys()}


class LocationStatsListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        serializer = MultiLocationStatsSerializer()
        return  Response(serializer.data)
from rest_framework import serializers
from rest_framework_mongoengine.generics import ListAPIView
from rest_framework.response import Response

from dms.services.location_stats import MultiLocationStatsService


class StatsDetailsSerializer(serializers.Serializer):

    count = serializers.Field()
    percentage = serializers.Field()


class LocationStatsSerializer(serializers.Serializer):

    messages = StatsDetailsSerializer(many=False)
    disasters = StatsDetailsSerializer(many=False)


class MultiLocationStatsSerializer(object):

    def __init__(self, district_name=None, from_date=None, to_date=None):
        self.stats = MultiLocationStatsService(district_name, from_date, to_date).stats()
        self.data = self._serialized_data()

    def _serialized_data(self):
        return {location_name.lower(): LocationStatsSerializer(self.stats[location_name]).data for location_name in self.stats.keys()}


class LocationStatsListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        from_date = request.GET.get('from', None)
        to_date = request.GET.get('to', None)
        serializer = MultiLocationStatsSerializer(from_date=from_date, to_date=to_date)
        return Response(serializer.data)


class DistrictStatsListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        from_date = request.GET.get('from', None)
        to_date = request.GET.get('to', None)
        district = kwargs.get('district', None)
        serializer = MultiLocationStatsSerializer(district, from_date, to_date)
        return Response(serializer.data)

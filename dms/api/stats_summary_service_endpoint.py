from rest_framework import serializers
from rest_framework_mongoengine.generics import ListAPIView
from rest_framework.response import Response

from dms.models import Location
from dms.services.stats_summary import StatsSummaryService


class SummaryStatsDetailsSerializer(serializers.Serializer):

    count = serializers.Field()
    affected = serializers.Field()
    types = serializers.Field()


class SummaryStatsSerializer(serializers.Serializer):

    disasters = SummaryStatsDetailsSerializer(many=False)


class SummaryStatsListView(ListAPIView):

    def get_location(self, kwargs):
        location_name = kwargs.get('subcounty') or kwargs.get('district') or kwargs.get('location')
        if location_name:
            return Location.objects(name__iexact=location_name.lower()).first()

    def get_service(self, request):
        kwargs = request.GET.dict()
        kwargs['location'] = self.get_location(kwargs)
        return StatsSummaryService(**kwargs)

    def list(self, request, *args, **kwargs):
        service = self.get_service(request)
        serializer = SummaryStatsSerializer(service.aggregate_stats())
        return Response(serializer.data)

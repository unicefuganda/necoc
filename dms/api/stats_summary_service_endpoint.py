from rest_framework import serializers
from rest_framework_mongoengine.generics import ListAPIView
from rest_framework.response import Response

from dms.services.location_stats import MultiLocationStatsService


class SummaryStatsDetailsSerializer(serializers.Serializer):

    count = serializers.Field()
    affected = serializers.Field()
    types = serializers.Field()


class SummaryStatsSerializer(serializers.Serializer):

    disasters = SummaryStatsDetailsSerializer(many=False)


from mongoengine.django.auth import Group
from rest_framework.response import Response
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView, ListAPIView


class GroupSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Group
        exclude = ('permissions',)


class GroupsEndpointListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        queryset = Group.objects()
        data = [GroupSerializer(query).data for query in queryset]
        return Response(data)
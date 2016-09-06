from django.conf import settings
from rest_condition import Or
from rest_framework import fields
from rest_framework.settings import api_settings
from rest_framework_csv.renderers import CSVRenderer

from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models import UserProfile

from dms.models.disaster import Disaster
from dms.utils.permission_class_factory import IsGetRequest, build_permission_class
from dms.utils.user_profile_utils import get_user_district_locations
from rest_framework import serializers as serialiserzz


class DisasterSerializer(serializers.MongoEngineModelSerializer):
    status = fields.ChoiceField(source='status', choices=Disaster.DISASTER_STATUS)

    class Meta:
        model = Disaster
        depth = 4
        exclude = ('created_at',)


class DisasterListCreateView(ListCreateAPIView):
    model = Disaster
    serializer_class = DisasterSerializer
    queryset = Disaster.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_disasters'), IsGetRequest)]

    def get_queryset(self):
        query_params = Disaster.map_kwargs_to_db_params(self.request.GET.dict())

        location_queried = self.request.GET.get('location', None)
        if not location_queried:
            if self.request.user.has_perm('dms.can_view_disasters') and \
                    not self.request.user.has_perm('dms.can_manage_disasters'):
                user_profile = UserProfile.objects(user=self.request.user).first()
                user_group = self.request.user.group.name
                if user_profile and user_group in getattr(settings, 'DISTRICT_GROUPS', []):
                    user_locations = get_user_district_locations(self.request.user)
                    query_params.update({'locations__in': user_locations})
                else:
                    user_location = user_profile.location.id
                    query_params.update({'locations__in':[user_location]})

        return Disaster.objects(**query_params)


class DisasterView(MongoRetrieveUpdateView):
    model = Disaster
    serializer_class = DisasterSerializer
    queryset = Disaster.objects()
    permission_classes = [Or(build_permission_class('dms.can_view_disasters'))]

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)


class CSVDisasterSerializer(serializers.MongoEngineModelSerializer):
    name = serialiserzz.Field(source='csv_name')
    status = fields.ChoiceField(source='status', choices=Disaster.DISASTER_STATUS)
    location = serialiserzz.Field(source='csv_locations', label='Locations')

    class Meta:
        model = Disaster
        depth = 4
        exclude = ('id', 'created_at', 'locations')


class CSVDisasterView(ListCreateAPIView):
    model = Disaster
    serializer_class = CSVDisasterSerializer
    queryset = Disaster.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_disasters'), IsGetRequest)]
    renderer_classes = [CSVRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES

    def get_queryset(self):
        params = self._filter_params(self.request)
        queryset = Disaster.objects.filter(**params)
        return queryset.order_by('-created_at')

    def _filter_params(self, req):
        start_date = req.GET.get('from')
        end_date = req.GET.get('to')
        status = req.GET.get('status')
        params = {}

        if start_date:
            if not self._undefined(start_date):
                params.update({'date__gte' : start_date})

        if end_date:
            if not self._undefined(end_date):
                params.update({'date__lte' : end_date})

        if status:
            if not self._undefined(status):
                params.update({'status':status})

        return params

    def _undefined(self, strValue):
        return strValue == u'undefined'
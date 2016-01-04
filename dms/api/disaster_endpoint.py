from rest_condition import Or
from rest_framework import fields

from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models import UserProfile

from dms.models.disaster import Disaster
from dms.utils.permission_class_factory import IsGetRequest, build_permission_class


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
                if user_profile:
                    user_location = user_profile.location.id
                    query_params.update({'locations__in':[user_location]})

        return Disaster.objects(**query_params)


class DisasterView(MongoRetrieveUpdateView):
    model = Disaster
    serializer_class = DisasterSerializer
    queryset = Disaster.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_disasters'))]

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
from rest_condition import And, Or
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework import serializers as rest_serializers

from dms.models import Poll, Location, UserProfile
from dms.tasks import send_bulk_sms
from dms.utils.general_helpers import flatten
from dms.utils.permission_class_factory import build_permission_class, IsGetRequest


class PollSerializer(serializers.MongoEngineModelSerializer):
    created_at = fields.DateTimeField(source='created_at', required=False)
    number_of_responses = serialiserzz.Field(source='number_of_responses')
    yesno_poll_stats = serialiserzz.Field(source='yesno_poll_stats')
    participants = serialiserzz.Field(source='number_of_participants')

    def validate_keyword(self, attrs, source):
        if len(Poll.objects(keyword=attrs[source])):
            raise rest_serializers.ValidationError('Keyword must be unique')
        return attrs

    class Meta:
        model = Poll
        exclude = ('log',)


class PollListCreateView(ListCreateAPIView):
    model = Poll
    serializer_class = PollSerializer
    queryset = Poll.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_polls'),
                             And(build_permission_class('dms.can_view_polls'), IsGetRequest))]

    def get_queryset(self):
        query_params = {key: value or None for key, value in self.request.GET.items()}
        if 'ordering' in query_params:
            ordering_params = query_params['ordering']
            del query_params['ordering']
            query_set = Poll.objects(**query_params).order_by('%s' % ordering_params)
        else:
            query_set = Poll.objects(**query_params).order_by('-created_at')
        return query_set

    def post_save(self, obj, created=True):
        locations = self.get_location(obj)
        phone_numbers = list(UserProfile.objects(location__in=locations).values_list('phone'))
        text = '%s Reply With: %s' % (obj.question, obj.keyword)
        send_bulk_sms.delay(obj, phone_numbers, text)

    def get_location(self, obj):
        locations = Location.objects(id__in=obj.target_locations)
        if locations.filter(type='subcounty'):
            return locations
        districts_children = [district.children() for district in locations]
        return flatten(districts_children)
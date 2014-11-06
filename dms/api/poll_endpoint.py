from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework import serializers as serialiserzz
from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework import serializers as rest_serializers
from dms.models import Poll, Location, UserProfile
from dms.tasks import send_bulk_sms
from dms.utils.general_helpers import flatten


class PollSerializer(serializers.MongoEngineModelSerializer):
    created_at = fields.DateTimeField(source='created_at', required=False)
    number_of_responses = serialiserzz.Field(source='number_of_responses')

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

    def post_save(self, obj, created=True):
        locations = self.get_location(obj)
        phone_numbers = list(UserProfile.objects(location__in=locations).values_list('phone'))
        text = '%s Reply With: %s' % (obj.question, obj.keyword)
        send_bulk_sms.delay(obj, phone_numbers, text)

    def get_location(self, obj):
        locations = Location.objects(id__in=obj.target_locations)
        if locations.filter(type='sub_county'):
            return locations
        districts_children = [district.children() for district in locations]
        return flatten(districts_children)
from rest_framework_mongoengine import serializers
from rest_framework import fields
from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework import serializers as rest_serializers
from dms.models import Poll, Location, MobileUser
from dms.tasks import send_bulk_sms


class PollSerializer(serializers.MongoEngineModelSerializer):
    created_at = fields.DateTimeField(source='created_at', required=False)

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
        locations = Location.objects(id__in=obj.target_locations)
        phone_numbers = list(MobileUser.objects(location__in=locations).values_list('phone'))
        text = '%s Reply With: %s' % (obj.question, obj.keyword)
        send_bulk_sms.delay(obj, phone_numbers, text)
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView
from dms.models import Poll, Location, MobileUser
from dms.tasks import send_bulk_sms


class PollSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Poll
        exclude = ('created_at',)


class PollListCreateView(ListCreateAPIView):
    model = Poll
    serializer_class = PollSerializer
    queryset = Poll.objects()

    def post_save(self, obj, created=True):
        locations = Location.objects(id__in=obj.target_locations)
        phone_numbers = MobileUser.objects(location=locations).values_list('phone')
        text = '%s Respond With: %s' % (obj.question, obj.keyword)
        send_bulk_sms.delay(obj, phone_numbers, text)
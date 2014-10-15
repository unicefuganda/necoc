from django.conf import settings
from mongoengine import *

from dms.models.message import ReceivedMessage
from dms.models.mobile_user import MobileUser
from dms.utils.location_utils import find_location_match
from dms.utils.rapidpro_message_utils import clean_text


class RapidProMessage (ReceivedMessage):
    SENDER = 'NECOC Volunteer'
    relayer_id = IntField()
    run_id = IntField()

    def __init__(self, *args, **kwargs):
        super(RapidProMessage, self).__init__(*args, **kwargs)
        self.location = self._assign_location()

    def source(self):
        return self.SENDER

    def mobile_user(self):
        return MobileUser.objects(phone=self.phone_no).first()

    def _assign_location(self):
        text = clean_text(self.text)
        return find_location_match(text[settings.MESSAGE_LOCATION_INDEX-1])

    def location_str(self):
        if self.location:
            return str(self.location)
        return ""

    @classmethod
    def from_(cls, location, _queryset=None):
        if not _queryset:
            _queryset = cls.objects()
        locations = location.children(include_self=True)
        return _queryset.filter(location__in=locations)

    class Meta:
        app_label = 'dms'

from django.conf import settings
from mongoengine import *
from dms.models import Poll

from dms.models.message import RapidProMessageBase
from dms.utils.rapidpro_message_utils import clean_text


class PollResponse(RapidProMessageBase):
    poll = ReferenceField('Poll')

    def _assign_location(self):
        mobile_user = self.mobile_user()
        if mobile_user:
            return mobile_user.location

    def save(self, *args, **kwargs):
        self.poll = self.poll or self._assign_poll()
        return super(PollResponse, self).save(*args, **kwargs)

    def _assign_poll(self):
        text = clean_text(self.text)
        if len(text) > settings.POLL_RESPONSE_LOCATION_INDEX-1:
            keyword = text[settings.POLL_RESPONSE_LOCATION_INDEX - 1]
            return Poll.objects(keyword=keyword).first()
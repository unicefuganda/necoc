import re
from django.conf import settings
from mongoengine import *
from dms.models.poll import Poll

from dms.models.message import RapidProMessageBase
from dms.utils.rapidpro_message_utils import split_text


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
        text = self.split_text()
        if len(text) > settings.POLL_RESPONSE_KEYWORD_INDEX-1:
            keyword = text[settings.POLL_RESPONSE_KEYWORD_INDEX - 1]
            return Poll.objects(keyword=keyword).first()

    def split_text(self):
        try:
            split_message = re.findall(r"[\w']+", self.text)
        except TypeError:
            split_message = []
        return map(lambda x: x.strip(), split_message)

    def poll_name(self):
        if self.poll:
            return self.poll.name

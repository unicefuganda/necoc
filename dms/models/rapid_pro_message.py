from django.conf import settings
from mongoengine import *

from dms.models.message import RapidProMessageBase
from dms.utils.location_utils import find_location_match
from dms.utils.rapidpro_message_utils import split_text


class RapidProMessage(RapidProMessageBase):
    disaster = ReferenceField('Disaster')

    def _assign_location(self):
        if self.text:
            text = split_text(self.text)
            if len(text) > settings.MESSAGE_LOCATION_INDEX-1:
                return find_location_match(text[settings.MESSAGE_LOCATION_INDEX-1])

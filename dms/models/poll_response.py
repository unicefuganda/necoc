from mongoengine import *

from dms.models.message import RapidProMessageBase


class PollResponse(RapidProMessageBase):
    poll = ReferenceField('Poll')

    def _assign_location(self):
        mobile_user = self.mobile_user()
        if mobile_user:
            return mobile_user.location
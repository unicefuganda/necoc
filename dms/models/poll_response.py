from dms.models import RapidProMessage
from mongoengine import *


class PollResponse(RapidProMessage):
    poll = ReferenceField('Poll')

    def _assign_location(self):
        mobile_user = self.mobile_user()
        if mobile_user:
            return mobile_user.location
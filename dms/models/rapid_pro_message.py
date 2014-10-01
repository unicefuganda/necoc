from dms.models.message import ReceivedMessage
from mongoengine import *
from dms.models.mobile_user import MobileUser


class RapidProMessage (ReceivedMessage):
    SENDER = 'NECOC Volunteer'
    relayer_id = IntField()
    run_id = IntField()

    def source(self):
        return self.SENDER

    def mobile_user(self):
        return MobileUser.objects(phone=self.phone_no).first()

    def location(self):
        mobile_user = self.mobile_user()
        if mobile_user:
            return mobile_user.location

    def location_str(self):
        location = self.location()
        if location:
            return str(location)
        return ""

    class Meta:
        app_label = 'dms'

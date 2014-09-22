from dms.models.message import Message
from mongoengine import *


class RapidProMessage (Message):
    SENDER = 'NECOC Volunteer'

    relayer_id = IntField()
    relayer_phone = StringField()
    sms_id = IntField()
    status = StringField()
    direction = StringField()
    event = StringField()

    def source(self):
        return self.SENDER

    class Meta:
        app_label = 'dms'

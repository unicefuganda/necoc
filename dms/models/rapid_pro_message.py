from dms.models.message import Message
from mongoengine import *


class RapidProMessage (Message):
    SENDER = 'NECOC Volunteer'
    relayer_id = IntField()
    run_id = IntField()

    def source(self):
        return self.SENDER

    class Meta:
        app_label = 'dms'

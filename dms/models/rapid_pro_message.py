from dms.models.message import Message
from mongoengine import *


class RapidProMessage (Message):
    relayer_id = IntField()
    relayer_phone = StringField()
    sms_id = IntField()
    status = StringField()
    direction = StringField()
    event = StringField()

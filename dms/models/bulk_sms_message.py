import mongoengine
from dms.models.message import Message


class SentMessage(Message):
    phone_numbers = mongoengine.ListField()
    log = mongoengine.StringField()
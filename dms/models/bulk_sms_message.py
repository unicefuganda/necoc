from mongoengine import ListField, IntField, StringField
from dms.models.message import Message


class SentMessage(Message):
    phone_numbers = ListField()
    log = StringField()
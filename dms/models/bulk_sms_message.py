from mongoengine import ListField
from dms.models.message import Message


class SentMessage(Message):
    phone_numbers = ListField()
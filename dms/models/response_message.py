import mongoengine
from dms.models.message import Message


class ResponseMessage(Message):
    phone_numbers = mongoengine.ListField()
    response_to = mongoengine.ReferenceField('SentMessage', required=False)
    log = mongoengine.StringField()
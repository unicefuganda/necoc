import mongoengine
from dms.models.message import Message


class ResponseMessage(Message):
    phone = mongoengine.StringField()
    response_to = mongoengine.StringField(required=False)
    log = mongoengine.StringField()
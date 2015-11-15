import mongoengine
from dms.models.message import Message


class ResponseMessage(Message):
    phone_number = mongoengine.StringField()
    response_to = mongoengine.ReferenceField('RapidProMessage', required=False)
    log = mongoengine.StringField()
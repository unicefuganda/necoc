from mongoengine import *
import datetime


class Message(Document):
    text = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True
    }


class ReceivedMessage(Message):
    phone_no = StringField()
    received_at = DateTimeField()
    disaster = ReferenceField('Disaster')
    location = ReferenceField('Location')

    meta = {
        'allow_inheritance': True
    }

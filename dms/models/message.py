from mongoengine import *
import datetime


class Message(Document):
    text = StringField()
    phone_no = StringField()
    received_at = DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True
    }

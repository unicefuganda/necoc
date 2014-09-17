from mongoengine import *


class Disaster(Document):
    name = StringField(max_length=200)
    description = StringField()

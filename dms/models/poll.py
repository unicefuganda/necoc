from dms.models.base import BaseModel
from mongoengine import *


class Poll(BaseModel):
    name = StringField()
    question = StringField(max_length=160)
    keyword = StringField(max_length=10, unique=True)
    target_locations = ListField()
    log = StringField()

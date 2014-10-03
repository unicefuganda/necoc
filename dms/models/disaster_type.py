from mongoengine import *
from dms.models.base import BaseModel


class DisasterType(BaseModel):
    name = StringField(max_length=200)
    description = StringField()

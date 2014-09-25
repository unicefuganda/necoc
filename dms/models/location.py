from mongoengine import *
from dms.models.base import BaseModel


class Location(BaseModel):
    name = StringField(required=True)
    type = StringField(required=True)
    parent = ReferenceField('self', required=False)
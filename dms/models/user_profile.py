from mongoengine import *
from mongoengine.django.auth import User
from dms.models.base import BaseModel
from dms.models.location import Location


class UserProfile(BaseModel):
    name = StringField(required=True)
    phone = StringField(required=True, unique=True)
    location = ReferenceField(Location, required=True)
    email = StringField()
    user = ReferenceField(User)
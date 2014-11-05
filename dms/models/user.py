from mongoengine import StringField, ReferenceField
from mongoengine.django.auth import User as MongoUser


class User(MongoUser):
    phone_no = StringField()
    location = ReferenceField('Location')

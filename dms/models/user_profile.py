import datetime
from mongoengine import *
from dms.models import User
from dms.models.base import BaseModel
from dms.models.location import Location


class MongoFileField(FileField):
    max_length = None


class UserProfile(BaseModel):
    name = StringField(required=True)
    phone = StringField(required=True, unique=True)
    location = ReferenceField(Location, required=True)
    email = StringField()
    photo = MongoFileField()
    user = ReferenceField(User)
    ordering = ['-created_at',]

    def __unicode__(self):
        return self.name

    def username(self):
        return self.user.username if self.user else ''

    def user_id(self):
        return str(self.user.id) if self.user else ''

    def group(self):
        has_group = self.user and self.user.group
        return self.user.group.id if has_group else ''

    def group_name(self):
        has_group = self.user and self.user.group
        return self.user.group.name if has_group else ''

    def photo_uri(self):
        if self.photo and self.id:
            return '/api/v1/photo/%s' % self.id
        return None

    def district(self):
        return self.location.find('district').name if self.location.find('district') else None

    def subcounty(self):
        return self.location.find('subcounty').name if self.location.find('subcounty') else None
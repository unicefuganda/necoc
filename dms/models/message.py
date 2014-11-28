import datetime
from mongoengine import *

from dms.models import UserProfile
from django.conf import settings


class Message(Document):
    text = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True
    }


class ReceivedMessage(Message):
    phone_no = StringField()
    received_at = DateTimeField()
    location = ReferenceField('Location')

    meta = {
        'allow_inheritance': True
    }


class RapidProMessageBase (ReceivedMessage):
    SENDER = 'NECOC Volunteer'
    relayer_id = IntField()
    run_id = IntField()
    MAPPING = {'from': 'received_at__gte', 'to': 'received_at__lte'}

    def save(self, *args, **kwargs):
        self.location = self.location or self._assign_location()
        return super(RapidProMessageBase, self).save(*args, **kwargs)

    def source(self):
        return self.SENDER

    def mobile_user(self):
        phone_no = self.phone_no.replace(settings.INTERNATIONAL_PHONE_PREFIX, '')
        return UserProfile.objects(phone=phone_no).first()

    def _assign_location(self):
        pass

    def location_str(self):
        if self.location:
            return str(self.location)
        return ""

    @classmethod
    def map_kwargs_to_db_params(cls, kwargs):
        return {value: kwargs.get(key) for key, value in cls.MAPPING.items() if kwargs.get(key, None)}

    @classmethod
    def from_(cls, location, _queryset=None, **kwargs):
        if not _queryset:
            _queryset = cls.objects()
        mapping = cls.map_kwargs_to_db_params(kwargs)
        mapping['location__in'] = location.children(include_self=True)
        return _queryset.filter(**mapping)

    @classmethod
    def count_(cls, **kwargs):
        mapping = cls.map_kwargs_to_db_params(kwargs)
        return cls.objects.filter(**mapping).count()

    class Meta:
        app_label = 'dms'

import datetime
from mongoengine import *
from dms.models import MobileUser


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

    def save(self, *args, **kwargs):
        self.location = self.location or self._assign_location()
        return super(RapidProMessageBase, self).save(*args, **kwargs)

    def source(self):
        return self.SENDER

    def mobile_user(self):
        return MobileUser.objects(phone=self.phone_no).first()

    def _assign_location(self):
        pass

    def location_str(self):
        if self.location:
            return str(self.location)
        return ""

    @classmethod
    def from_(cls, location, _queryset=None):
        if not _queryset:
            _queryset = cls.objects()
        locations = location.children(include_self=True)
        return _queryset.filter(location__in=locations)

    class Meta:
        app_label = 'dms'

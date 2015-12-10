from mongoengine import *

from dms.models.message import RapidProMessageBase
from dms.utils.location_utils import MessageLocationExtractor
from dms.utils.message_utils import MessageDisasterAssociator, MessageProfileLocationAssociator, \
    MessageTextLocationAssociator
from mongoengine import post_save
from dms.utils.signal_receivers import associate_disaster

class RapidProMessage(RapidProMessageBase):
    disaster = ReferenceField('Disaster')
    auto_associated = BooleanField(default=False)

    def _assign_location(self):
        mobile_user = self.mobile_user()
        if MessageTextLocationAssociator(self.text).best_match():
            return MessageTextLocationAssociator(self.text).best_match()
        else:
            return MessageProfileLocationAssociator(mobile_user).best_match()

    def _associate_to_disaster(self):
        return MessageDisasterAssociator(self.text).match_disaster()

    def disaster_str(self):
        if self.disaster:
            return self.disaster.name.name

    @classmethod
    def get_fields(cls):
        return cls._fields_ordered

    @classmethod
    def from_(cls, location, _queryset=None, **kwargs):
        _queryset = super(RapidProMessage, cls).from_(location, _queryset, **kwargs)
        return cls._filter_disaster_type(_queryset, kwargs)

    @classmethod
    def count_(cls, **kwargs):
        mapping = {value: kwargs.get(key) for key, value in cls.MAPPING.items() if kwargs.get(key, None)}
        _queryset = cls._filter_disaster_type(cls.objects(**mapping), kwargs)
        return _queryset.count()

    @classmethod
    def _filter_disaster_type(cls, _queryset, kwargs):
        if kwargs.get('disaster_type', None):
            from dms.models.disaster import Disaster
            disasters = Disaster.objects(name=kwargs['disaster_type'])
            if disasters:
                return _queryset.filter(disaster__in=disasters)
            return _queryset.none()
        return _queryset

post_save.connect(associate_disaster)
from django.conf import settings
from mongoengine import *

from dms.models.message import RapidProMessageBase
from dms.utils.location_utils import find_location_match
from dms.utils.rapidpro_message_utils import split_text


class RapidProMessage(RapidProMessageBase):
    disaster = ReferenceField('Disaster')

    def _assign_location(self):
        if self.text:
            text = split_text(self.text)
            if len(text) > settings.MESSAGE_LOCATION_INDEX-1:
                return find_location_match(text[settings.MESSAGE_LOCATION_INDEX-1])

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

from mongoengine import ReferenceField, StringField, DateTimeField, ListField
from dms.models.disaster_type import DisasterType
from dms.models.location import Location
from dms.models.base import BaseModel
from django.conf import settings


class Disaster(BaseModel):
    DISASTER_STATUS = [(status, status) for status in settings.DISASTER_STATUSES]

    MAPPING = {'from': 'date__gte', 'to': 'date__lte', 'disaster_type': 'name', 'status': 'status__iexact'}

    name = ReferenceField(DisasterType, required=True)
    locations = ListField(ReferenceField(Location))
    description = StringField()
    status = StringField(choices=DISASTER_STATUS)
    date = DateTimeField(required=True)

    @classmethod
    def map_kwargs_to_db_params(cls, kwargs):
        return {value: kwargs.get(key) for key, value in cls.MAPPING.items() if kwargs.get(key, None)}

    @classmethod
    def from_(cls, location=None, **kwargs):
        mapping = cls.map_kwargs_to_db_params(kwargs)
        if location:
            locations = location.children(include_self=True)
            mapping['locations__in'] = locations
        return cls.objects.filter(**mapping)

    @classmethod
    def count_(cls, **kwargs):
        queryset = cls.from_(**kwargs)
        return queryset.count()


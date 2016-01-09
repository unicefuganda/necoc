from mongoengine import ReferenceField, StringField, DateTimeField, ListField, pre_save
from dms.models.disaster_type import DisasterType
from dms.models.location import Location
from dms.models.base import BaseModel
from django.conf import settings
from dms.utils.signal_receivers import notify_new_disaster_status


class Disaster(BaseModel):
    DISASTER_STATUS = [(status, status) for status in settings.DISASTER_STATUSES]

    MAPPING = {'from': 'date__gte', 'to': 'date__lte', 'disaster_type': 'name', 'status': 'status__iexact'}

    name = ReferenceField(DisasterType, required=True)
    locations = ListField(ReferenceField(Location))
    description = StringField()
    status = StringField(choices=DISASTER_STATUS)
    date = DateTimeField(required=True)

    def __unicode__(self):
        return self.name.name

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

    def csv_locations(self):
        if self.locations:
            locations = []
            for loc in self.locations:
                locations.append(loc.name)
            return '|'.join(locations)

    def csv_name(self):
        return self.name.name

pre_save.connect(notify_new_disaster_status)


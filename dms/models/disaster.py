from mongoengine import ReferenceField, StringField, DateTimeField, ListField
from dms.models.disaster_type import DisasterType
from dms.models.location import Location
from dms.models.base import BaseModel


class Disaster(BaseModel):
    DISASTER_STATUS = (('Assessment', 'Assessment'), ('Evaluation', 'Evaluation'),
                       ('Response Team Deployed', 'Response Team Deployed'),
                       ('Closed', 'Closed'))

    MAPPING = {'from': 'date__gte', 'to': 'date__lte', 'disaster_type': 'name'}

    name = ReferenceField(DisasterType, required=True)
    locations = ListField(ReferenceField(Location))
    description = StringField()
    status = StringField(choices=DISASTER_STATUS)
    date = DateTimeField(required=True)

    @classmethod
    def from_(cls, location, **kwargs):
        locations = location.children(include_self=True)
        mapping = {value: kwargs.get(key) for key, value in cls.MAPPING.items() if kwargs.get(key, None)}
        mapping['locations__in'] = locations
        return cls.objects.filter(**mapping)

    @classmethod
    def count_(cls, **kwargs):
        mapping = {value: kwargs.get(key) for key, value in cls.MAPPING.items() if kwargs.get(key, None)}
        return cls.objects.filter(**mapping).count()


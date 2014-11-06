from mongoengine import ReferenceField, StringField, DateTimeField, ListField
from dms.models.disaster_type import DisasterType
from dms.models.location import Location
from dms.models.base import BaseModel


class Disaster(BaseModel):
    DISASTER_STATUS = (('Assessment', 'Assessment'), ('Evaluation', 'Evaluation'),
                       ('Response Team Deployed', 'Response Team Deployed'),
                       ('Closed', 'Closed'))

    MAPPING = dict(from_date='created_at__gte', to_date='created_at__lte')

    name = ReferenceField(DisasterType, required=True)
    locations = ListField(ReferenceField(Location))
    description = StringField()
    status = StringField(choices=DISASTER_STATUS)
    date = DateTimeField(required=True)

    @classmethod
    def from_(cls, location, **kwargs):
        locations = location.children(include_self=True)
        mapping = {cls.MAPPING[key]: value for key, value in kwargs.items() if value}
        mapping['locations__in'] = locations
        return cls.objects.filter(**mapping)

    @classmethod
    def count_(cls, **kwargs):
        mapping = {cls.MAPPING[key]: value for key, value in kwargs.items() if value}
        return cls.objects.filter(**mapping).count()


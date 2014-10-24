from mongoengine import ReferenceField, StringField, DateTimeField
from dms.models.disaster_type import DisasterType
from dms.models.location import Location
from dms.models.base import BaseModel


class Disaster(BaseModel):
    DISASTER_STATUS = (('Assessment', 'Assessment'), ('Evaluation', 'Evaluation'),
                       ('Response Team Deployed', 'Response Team Deployed'),
                       ('Closed', 'Closed'))

    name = ReferenceField(DisasterType, required=True)
    location = ReferenceField(Location, required=True)
    description = StringField()
    status = StringField(choices=DISASTER_STATUS)
    date = DateTimeField(required=True)

    @classmethod
    def from_(cls, location):
        locations = location.children(include_self=True)
        return cls.objects.filter(location__in=locations)

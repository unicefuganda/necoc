from mongoengine import ReferenceField, StringField, DateTimeField
from dms.models import DisasterType, Location
from dms.models.base import BaseModel


class Disaster(BaseModel):
    name = ReferenceField(DisasterType, required=True)
    location = ReferenceField(Location, required=True)
    description = StringField()
    status = StringField(choices=('Assessment', 'Evaluation', 'Response Team Deployed', 'Closed'))
    date = DateTimeField(required=True)
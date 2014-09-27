from mongoengine import *
from dms.models.base import BaseModel


class Location(BaseModel):
    name = StringField(required=True)
    type = StringField(required=True)
    parent = ReferenceField('self', required=False)

    def __unicode__(self):
        if self.parent and self.parent.name:
            return '%s >> %s'%(self.parent.name, self.name)
        return '%s'%self.name
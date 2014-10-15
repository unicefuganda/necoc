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

    def _children(self):
        return Location.objects(parent=self)

    def children(self, include_self=False):
        children = list(self._children())
        if not include_self:
            return self._children()
        children.insert(0, self)
        return children

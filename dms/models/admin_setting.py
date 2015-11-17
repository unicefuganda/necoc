__author__ = 'asseym'


from mongoengine import *
from dms.models.base import BaseModel


class AdminSetting(BaseModel):
    name = StringField(max_length=200, unique=True)
    yes_no = BooleanField(default=True, verbose_name='Yes/No')
    value_str = StringField(required=False)
    value_int = IntField(required=False)

    meta = {
        'app_label': 'dms',
    }

    def __unicode__(self):
        return self.name

    @classmethod
    def _lookup(cls, setting):
        try:
            return cls.objects.get(name=setting)
        except DoesNotExist:
            return None
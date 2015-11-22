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

    @classmethod
    def _set_attr(cls, setting, new_value, attribute='yes_no'):
        setting.__setattr__(attribute, new_value)
        setting.save()

    @classmethod
    def _set(cls, setting_name, new_value):
        setting = cls._lookup(str(setting_name))
        if setting:
            if type(new_value) == bool:
                cls._set_attr(setting, new_value)
            elif type(new_value) == str:
                cls._set_attr(setting, new_value, 'value_str')
            else:
                cls._set_attr(setting, new_value, 'value_int')
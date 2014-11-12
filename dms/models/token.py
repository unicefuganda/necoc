import binascii
import os
from mongoengine import StringField, ReferenceField
from dms.models import User
from dms.models.base import BaseModel


class Token(BaseModel):
    key = StringField(max_length=40, primary_key=True)
    user = ReferenceField(User, required=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.key
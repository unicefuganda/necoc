from mongoengine import *

from dms.models.base import BaseModel


class Poll(BaseModel):
    name = StringField()
    question = StringField(max_length=160)
    keyword = StringField(max_length=10, unique=True)
    target_locations = ListField()
    log = StringField()

    def responses(self):
        from dms.models import PollResponse
        return PollResponse.objects(poll=self)

    def number_of_responses(self):
        return self.responses().count()
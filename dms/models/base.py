from mongoengine import Document, DateTimeField
import datetime


class BaseModel(Document):
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'abstract': True,
    }
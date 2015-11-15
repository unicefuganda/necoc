import datetime
from dms.models.response_message import ResponseMessage

from dms.tests.base import MongoTestCase


class TestResponseMessage(MongoTestCase):

    def setUp(self):
        created_date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone = "+256775019449"
        self.message = dict(phone=phone, text="There is a fire", created_at=created_date_time,
                            log="haha")

    def test_save_sent_message(self):
        ResponseMessage(**self.message).save()
        sent_messages = ResponseMessage.objects(**self.message)
        self.assertEqual(1, sent_messages.count())


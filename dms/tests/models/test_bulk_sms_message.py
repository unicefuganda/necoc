import datetime

from dms.models.bulk_sms_message import SentMessage
from dms.tests.base import MongoTestCase


class TestSentMessage(MongoTestCase):

    def setUp(self):
        created_date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_numbers = ["+256775019449", "2345"]
        self.message = dict(phone_numbers=phone_numbers, text="There is a fire", created_at=created_date_time,
                            error_message="haha", rapid_pro_id="1234")

    def test_save_sent_message(self):
        SentMessage(**self.message).save()
        sent_messages = SentMessage.objects(**self.message)
        self.assertEqual(1, sent_messages.count())


import datetime

from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoTestCase


class TestRapidProMessage(MongoTestCase):

    def setUp(self):
        RapidProMessage.drop_collection()

    def tearDown(self):
        RapidProMessage.drop_collection()

    def test_save_rapid_pro_message(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        message = dict(phone_no="+256775019449", text="There is a fire", received_at=date_time, relayer_id=234,
                       relayer_phone="+256773434324", sms_id=23243, status="Q", direction="I", event="mo_sms")

        RapidProMessage(**message).save()
        rp_messages = RapidProMessage.objects(**message)
        self.assertEqual(1, rp_messages.count())
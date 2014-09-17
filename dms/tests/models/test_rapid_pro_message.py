import datetime

from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import NoSQLTestCase


class TestRapidProMessage(NoSQLTestCase):

    def tearDown(self):
        RapidProMessage.drop_collection()

    def test_save_rapid_pro_message(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        message = dict(phone_no="+256775019449", text="There is a fire", received_at=date_time, relayer_id=234,
                       relayer_phone="+256773434324", sms_id=23243, status="Q", direction="I", event="mo_sms")

        RapidProMessage(**message).save()
        rp_messages = RapidProMessage.objects()
        self.assertEqual(1, rp_messages.count())

        rp_message = rp_messages[0]
        self.assertEqual(rp_message['phone_no'], message['phone_no'])
        self.assertEqual(rp_message['text'], message['text'])
        self.assertEqual(rp_message['received_at'], date_time)
        self.assertEqual(rp_message['relayer_id'], message['relayer_id'])
        self.assertEqual(rp_message['relayer_phone'], message['relayer_phone'])
        self.assertEqual(rp_message['sms_id'], message['sms_id'])
        self.assertEqual(rp_message['status'], message['status'])
        self.assertEqual(rp_message['direction'], message['direction'])
        self.assertEqual(rp_message['event'], message['event'])


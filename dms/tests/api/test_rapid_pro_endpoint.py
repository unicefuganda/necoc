import datetime
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import NoSQLAPITestCase


class RapidProEndPointTest(NoSQLAPITestCase):

    def tearDown(self):
        RapidProMessage.drop_collection()

    def test_should_create_rapidpro_message(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        message = dict(phone_no="+256775019449", text="There is a fire", received_at=date_time, relayer_id=234,
                       relayer_phone="+256773434324", sms_id=23243, status="Q", direction="I", event="mo_sms")

        response = self.client.post('/api/v1/rapid-pro/', data=message)
        self.assertEqual(201, response.status_code)

        retrieved_message = RapidProMessage.objects(**message)
        self.assertEqual(1, retrieved_message.count())

    def test_should_get_rapidpro_message(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        message = dict(phone_no="+256775019449", text="There is a fire", received_at=date_time, relayer_id=234,
                       relayer_phone="+256773434324", sms_id=23243, status="Q", direction="I", event="mo_sms")

        RapidProMessage(**message).save()

        response = self.client.get('/api/v1/rapid-pro/', format='json')
        self.assertEqual(200, response.status_code)
        self.assertDictContainsSubset(message, response.data[0])
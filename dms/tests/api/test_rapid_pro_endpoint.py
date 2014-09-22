import datetime
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import NoSQLAPITestCase


class RapidProEndPointTest(NoSQLAPITestCase):

    API_ENDPOINT = '/api/v1/rapid-pro/'

    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.expected_message = dict(phone="+256775019449", text="There is a fire", time=date_time, relayer=234,
                                     relayer_phone="+256773434324", sms=23243, status="Q", direction="I",
                                     event="mo_sms")
        self.message = dict(phone_no="+256775019449", text="There is a fire", received_at=date_time, relayer_id=234,
                            relayer_phone="+256773434324", sms_id=23243, status="Q", direction="I", event="mo_sms")

    def tearDown(self):
        RapidProMessage.drop_collection()

    def test_should_create_rapid_pro_message(self):
        response = self.client.post(self.API_ENDPOINT, data=self.expected_message)
        self.assertEqual(201, response.status_code)

        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())

    def test_should_get_rapid_pro_message(self):
        RapidProMessage(**self.message).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.expected_message, response.data[0])
        self.assertEqual('NECOC Volunteer', response.data[0]['source'])
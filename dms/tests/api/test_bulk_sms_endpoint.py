import json
from dms.models import SentMessage
from dms.tests.base import MongoAPITestCase


class TestLocationEndpoint(MongoAPITestCase):

    BULK_SMS_ENDPOINT = '/api/v1/sent-messages/'

    def setUp(self):
        phone_numbers = ['256775019449', '2345']
        self.bulk_sms_to_post = dict(text="There is a fire", phone_numbers=phone_numbers)

    # TODO: NavaL and Mukiza Mock this ***t
    def test_should_post_sent_bulk_messages(self):
        data = json.dumps(self.bulk_sms_to_post)

        response = self.client.post(self.BULK_SMS_ENDPOINT, data=data, content_type="application/json")
        self.assertEqual(201, response.status_code)

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())

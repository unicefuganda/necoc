from httplib import HTTPException
import json
from dms.models import SentMessage
from dms.tests.base import MongoAPITestCase
from httmock import all_requests, HTTMock


class TestLocationEndpoint(MongoAPITestCase):

    BULK_SMS_ENDPOINT = '/api/v1/sent-messages/'

    def setUp(self):
        phone_numbers = ['256775019449', '2345']
        self.bulk_sms_to_post = dict(text="There is a fire", phone_numbers=phone_numbers)

    def test_should_post_sent_bulk_messages_and_save_returned_ids(self):
        data = json.dumps(self.bulk_sms_to_post)

        with HTTMock(self.post_successful):
            response = self.client.post(self.BULK_SMS_ENDPOINT, data=data, content_type="application/json")

        self.assertEqual(201, response.status_code)

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertEqual(6839436, retrieved_sms[0].rapid_pro_id)
        self.assertIsNone(retrieved_sms[0].error_message)

    def test_should_save_exception_message(self):
        data = json.dumps(self.bulk_sms_to_post)

        with HTTMock(self.post_throws_exception):
            response = self.client.post(self.BULK_SMS_ENDPOINT, data=data, content_type="application/json")

        self.assertEqual(201, response.status_code)

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertIsNone(retrieved_sms[0].rapid_pro_id)
        self.assertEqual("I do not accept your message", retrieved_sms[0].error_message)

    @all_requests
    def post_successful(self, url, request):
        rapid_pro_id = 6839436
        return {'status_code': 201,
                'content': {"messages": [rapid_pro_id], "sms": [rapid_pro_id]}
                }

    @all_requests
    def post_throws_exception(self, url, request):
        raise HTTPException('I do not accept your message')

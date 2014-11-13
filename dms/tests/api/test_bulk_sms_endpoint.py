import json

from mock import patch, MagicMock
from requests import RequestException

from dms.models import SentMessage
from dms.tests.base import MongoAPITestCase
from necoc.settings import API_URL, API_TOKEN


class TestLocationEndpoint(MongoAPITestCase):

    BULK_SMS_ENDPOINT = '/api/v1/sent-messages/'

    def setUp(self):
        self.login_user()
        phone_numbers = ['256775019449', '2345']
        self.bulk_sms_to_post = dict(text="There is a fire", phone_numbers=phone_numbers)
        self.headers = {'Authorization': 'Token ' + API_TOKEN,
                        'content-type': 'application/json'}

    @patch('dms.tasks.requests')
    def test_should_post_sent_bulk_messages_and_save_logs(self, mock_requests):
        success_log = '201: rapid_pro_id = 1234'
        some_id = 1234
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"messages": [some_id], "sms": [some_id]}
        mock_requests.post.return_value = mock_response
        data = json.dumps(self.bulk_sms_to_post)

        response = self.client.post(self.BULK_SMS_ENDPOINT, data=data, content_type="application/json")

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.bulk_sms_to_post), self.headers))
        self.assertEqual(201, response.status_code)

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertEqual(success_log, retrieved_sms[0].log)

    @patch('dms.tasks.requests')
    def test_should_save_exception_message(self, mock_requests):
        some_error = 'I do not accept your message'
        mock_requests.post.side_effect = RequestException(some_error)

        data = json.dumps(self.bulk_sms_to_post)

        response = self.client.post(self.BULK_SMS_ENDPOINT, data=data, content_type="application/json")

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.bulk_sms_to_post), self.headers))
        self.assertEqual(201, response.status_code)

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertEqual("RequestException: %s" % some_error, retrieved_sms[0].log)

    def test_should_get_rapid_pro_message(self):
        SentMessage(**self.bulk_sms_to_post).save()

        response = self.client.get(self.BULK_SMS_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.bulk_sms_to_post, response.data[0])

    def test_can_get_a_list_of_disaster_types_with_no_permissions(self):
        self.login_without_permissions()
        response = self.client.get(self.BULK_SMS_ENDPOINT)
        self.assertEquals(response.status_code, 200)

    def test_cant_post_to_disaster_types_without_permission(self):
        self.assert_permission_required_for_post(self.BULK_SMS_ENDPOINT)

    def test_can_post_to_disaster_types_with_permission(self):
        self.login_with_permission('can_manage_messages')
        response = self.client.get(self.BULK_SMS_ENDPOINT)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(self.BULK_SMS_ENDPOINT,
                                    data=json.dumps(self.bulk_sms_to_post),
                                    content_type="application/json")
        self.assertEqual(201, response.status_code)


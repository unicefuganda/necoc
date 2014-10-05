import json

from mock import patch, MagicMock
from requests.exceptions import ConnectTimeout, ConnectionError

from dms.models import SentMessage
from dms.tasks import send_bulk_sms
from dms.tests.base import MongoAPITestCase
from necoc.settings import API_TOKEN, API_URL


class CeleryTasksTest(MongoAPITestCase):

    def setUp(self):
        phone_numbers = ['256775019449', '2345']
        self.bulk_sms_to_post = dict(text="There is a fire", phone_numbers=phone_numbers)
        self.headers = {'Authorization': 'Token ' + API_TOKEN,
                        'content-type': 'application/json'}


    @patch('dms.tasks.requests')
    def test_should_send_message(self, mock_requests):
        sent_message_obj = SentMessage(**self.bulk_sms_to_post).save()
        some_id = 1234
        request_post = MagicMock()
        request_post.status_code = 201
        request_post.json.return_value = {"messages": [some_id], "sms": [some_id]}
        mock_requests.post.return_value = request_post

        send_bulk_sms(sent_message_obj)

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.bulk_sms_to_post), self.headers))

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertEqual(some_id, retrieved_sms[0].rapid_pro_id)
        self.assertIsNone(retrieved_sms[0].error_message)

    @patch('dms.tasks.requests')
    def test_non_201_responses_are_logged(self, mock_requests):
        sent_message_obj = SentMessage(**self.bulk_sms_to_post).save()
        some_id = 1234
        request_post = MagicMock()
        request_post.status_code = 400
        request_post.json.return_value = {"text": "This field is required."}
        mock_requests.post.return_value = request_post

        send_bulk_sms(sent_message_obj)

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.bulk_sms_to_post), self.headers))

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertIsNone(retrieved_sms[0].rapid_pro_id)
        self.assertEqual("400: {'text': 'This field is required.'}", retrieved_sms[0].error_message)

    @patch('dms.tasks.requests')
    def test_invalid_token(self, mock_requests):
        sent_message_obj = SentMessage(**self.bulk_sms_to_post).save()
        some_id = 1234
        request_post = MagicMock()
        request_post.status_code = 403
        request_post.json.return_value = {u'detail': u'Invalid token'}
        mock_requests.post.return_value = request_post

        send_bulk_sms(sent_message_obj)

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.bulk_sms_to_post), self.headers))

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertIsNone(retrieved_sms[0].rapid_pro_id)
        self.assertEqual("403: {u'detail': u'Invalid token'}", retrieved_sms[0].error_message)

    @patch('dms.tasks.requests')
    def test_rapid_pro_api_server_down_is_logged(self, mock_requests):
        sent_message_obj = SentMessage(**self.bulk_sms_to_post).save()
        network_error = 'rapid-pro server not responding in time'
        mock_requests.post.side_effect = ConnectTimeout(network_error)

        send_bulk_sms(sent_message_obj)

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.bulk_sms_to_post), self.headers))

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertIsNone(retrieved_sms[0].rapid_pro_id)
        self.assertEqual("ConnectTimeout: %s" % network_error, retrieved_sms[0].error_message)

    @patch('dms.tasks.requests')
    def test_domain_name_does_not_exists_is_logged(self, mock_requests):
        sent_message_obj = SentMessage(**self.bulk_sms_to_post).save()
        connection_error = 'Connection aborted. nodename nor servname provided, not known'
        mock_requests.post.side_effect = ConnectionError(connection_error)

        send_bulk_sms(sent_message_obj)

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.bulk_sms_to_post), self.headers))

        retrieved_sms = SentMessage.objects(**self.bulk_sms_to_post)
        self.assertEqual(1, retrieved_sms.count())
        self.assertIsNone(retrieved_sms[0].rapid_pro_id)
        self.assertEqual("ConnectionError: %s" % connection_error, retrieved_sms[0].error_message)

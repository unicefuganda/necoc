import json

from mock import patch, MagicMock
from requests import RequestException

from dms.models import ResponseMessage, AdminSetting
from dms.tests.base import MongoAPITestCase
from necoc import settings
from necoc.settings import API_URL, API_TOKEN


class TestResponseMessagepoint(MongoAPITestCase):

    RESPONSE_MESSAGE_ENDPOINT = '/api/v1/response-messages/'

    def setUp(self):
        self.login_user()
        phone = '+256775019449'
        self.response_text = settings.AUTO_RESPONSE_MESSAGE
        self.response_message_to_post = dict(text='some random text', phone=phone)
        self.response_message_to_retrieve = dict(text=self.response_text, phone=phone)
        self.headers = {'Authorization': 'Token ' + API_TOKEN,
                        'content-type': 'application/json'}
        AdminSetting(**dict(name='enable_automatic_response')).save()

    @patch('dms.tasks.requests')
    def test_should_post_response_messages_and_save_logs(self, mock_requests):
        success_log = '201: rapid_pro_id = 1234'
        some_id = 1234
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"messages": [some_id], "sms": [some_id]}
        mock_requests.post.return_value = mock_response
        data = json.dumps(self.response_message_to_post)

        response = self.client.post(self.RESPONSE_MESSAGE_ENDPOINT, data=data, content_type="application/json")

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.response_message_to_post), self.headers))
        self.assertEqual(201, response.status_code)

        retrieved_sms = ResponseMessage.objects(**self.response_message_to_retrieve)
        self.assertEqual(1, retrieved_sms.count())
        self.assertEqual(success_log, retrieved_sms[0].log)

    @patch('dms.tasks.requests')
    def test_should_post_with_alternate_authentication(self, mock_requests):
        success_log = '201: rapid_pro_id = 1234'
        some_id = 1234
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"messages": [some_id], "sms": [some_id]}
        mock_requests.post.return_value = mock_response
        data = json.dumps(self.response_message_to_post)

        response = self.client.post(self.RESPONSE_MESSAGE_ENDPOINT +'/?step=somestring', data=data, content_type="application/json")
        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.response_message_to_post), self.headers))
        # self.assertEqual(201, response.status_code)
        #
        # retrieved_sms = ResponseMessage.objects(**self.response_message_to_retrieve)
        # self.assertEqual(1, retrieved_sms.count())
        # self.assertEqual(success_log, retrieved_sms[0].log)

    @patch('dms.tasks.requests')
    def test_should_save_exception_message(self, mock_requests):
        some_error = 'I do not accept your message'
        mock_requests.post.side_effect = RequestException(some_error)

        data = json.dumps(self.response_message_to_post)

        response = self.client.post(self.RESPONSE_MESSAGE_ENDPOINT, data=data, content_type="application/json")

        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.response_message_to_post), self.headers))
        self.assertEqual(201, response.status_code)

        retrieved_sms = ResponseMessage.objects(**self.response_message_to_retrieve)
        self.assertEqual(1, retrieved_sms.count())
        self.assertEqual("RequestException: %s" % some_error, retrieved_sms[0].log)

    def test_should_get_response_message(self):
        ResponseMessage(**self.response_message_to_post).save()

        response = self.client.get(self.RESPONSE_MESSAGE_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.response_message_to_post, response.data[0])

    def test_can_get_a_list_of_response_messages_with_no_permissions(self):
        self.login_without_permissions()
        response = self.client.get(self.RESPONSE_MESSAGE_ENDPOINT)
        self.assertEquals(response.status_code, 200)

    def test_cant_post_to_response_messages_without_permission(self):
        self.assert_permission_required_for_post(self.RESPONSE_MESSAGE_ENDPOINT)

    def test_can_post_to_response_messages_with_permission(self):
        self.login_with_permission('can_manage_messages')
        response = self.client.get(self.RESPONSE_MESSAGE_ENDPOINT)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(self.RESPONSE_MESSAGE_ENDPOINT,
                                    data=json.dumps(self.response_message_to_post),
                                    content_type="application/json")
        self.assertEqual(201, response.status_code)


import json
from mock import patch, MagicMock
from dms.models import Poll, Location, MobileUser, PollResponse
from dms.tests.base import MongoAPITestCase
from necoc.settings import API_URL, API_TOKEN


class TestPollEndpoint(MongoAPITestCase):
    POLL_ENDPOINT = '/api/v1/polls/'

    def setUp(self):
        kampala = Location(**dict(name='Kampala', parent=None, type='district')).save()
        gulu = Location(**dict(name='Gulu', parent=None, type='district')).save()
        MobileUser(**(dict(name='timothy', phone='+256775019449', location=gulu, email=None))).save()

        self.target_locations = [str(kampala.id), str(gulu.id)]
        self.poll_to_post = dict(name="Disaster", question="How many disasters are in your area?", keyword="some_word",
                                 target_locations=self.target_locations)
        self.headers = {'Authorization': 'Token ' + API_TOKEN, 'content-type': 'application/json'}
        self.poll_to_send = dict(text='How many disasters are in your area? Reply with: POLL some_word',
                                 phone_numbers=['+256775019449'])

    # TODO: NavaL Figure this out:Mock.called_once_with
    @patch('dms.tasks.requests')
    def test_should_post_a_poll_and_save_logs(self, mock_requests):
        some_id = 1234
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"messages": [some_id], "sms": [some_id]}

        mock_requests.post.return_value = mock_response

        response = self.client.post(self.POLL_ENDPOINT, data=json.dumps(self.poll_to_post),
                                    content_type="application/json")
        self.assertEqual(201, response.status_code)
        self.assertTrue(mock_requests.post.called_once_with(API_URL, json.dumps(self.poll_to_send), self.headers))

        retrieved_poll = Poll.objects(**self.poll_to_post)
        self.assertEqual(1, retrieved_poll.count())

    def test_should_get_a_list_of_polls(self):
        poll = Poll(**self.poll_to_post).save()
        poll_response_attr = dict(phone_no='123455', text="NECOC There is a fire", relayer_id=234,
                        run_id=23243, poll=poll)

        PollResponse(**poll_response_attr).save()

        response = self.client.get(self.POLL_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        expected_poll = self.poll_to_post.copy()
        expected_poll['number_of_responses'] = 1
        self.assertDictContainsSubset(expected_poll, response.data[0])

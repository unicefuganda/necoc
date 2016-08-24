import json
import uuid
from django.test import override_settings
from mock import patch, MagicMock, ANY
from mongoengine.django.auth import Group, Permission, ContentType
from dms.models import Poll, Location, UserProfile, PollResponse, User
from dms.tests.base import MongoAPITestCase
from necoc.settings import API_URL, API_TOKEN


class TestPollEndpoint(MongoAPITestCase):
    POLL_ENDPOINT = '/api/v1/polls/'

    def setUp(self):
        self.login_user()
        self.kampala = Location(name='Kampala', parent=None, type='district').save()
        gulu = Location(**(dict(name='Gulu', parent=None, type='district'))).save()
        self.amuru = Location(**(dict(name='Amuru', parent=None, type='district'))).save()
        self.ddmc_group, created = Group.objects.get_or_create(name='DDMC')
        user_attr = dict(name='timothy', phone='+256775019449', location=gulu, email=None)
        UserProfile(**(user_attr)).save()

        self.bukoto = Location(name='Bukoto', parent=self.kampala, type='subcounty').save()
        bukoto_user_attr = dict(name='timothy', phone='+250775019449', location=self.bukoto, email=None)
        UserProfile(**bukoto_user_attr).save()
        bukoto_user_attr2 = bukoto_user_attr.copy()
        bukoto_user_attr2['phone'] = '+4343245552'
        UserProfile(**bukoto_user_attr2).save()

        self.target_locations = [str(self.kampala.id), str(gulu.id)]
        self.poll_to_post = dict(name="Disaster", question="How many disasters are in your area?", keyword="some_word",
                                 target_locations=self.target_locations)
        self.poll_to_post2 = dict(name="Disaster2", question="How many disasters are in your area?", keyword="some_word2",
                                  target_locations=[str(self.amuru.id)])
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

    @patch('dms.tasks.send_bulk_sms')
    def test_should_post_a_yesno_poll_and_resend_appropriate_outgoing_message(self, mock_send_bulk_sms):
        self.poll_to_post['question'] = 'Will you comply, yes or no?'
        self.poll_to_post['ptype'] = 'yesno'
        self.poll_to_send['text'] = 'Will you comply, yes or no? Reply With: NECOCPoll YES/NO'

        response = self.client.post(self.POLL_ENDPOINT, data=json.dumps(self.poll_to_post),
                                    content_type="application/json")
        self.assertEqual(201, response.status_code)
        # mock_send_bulk_sms.delay.assert_called_once_with(ANY, ANY, self.poll_to_send['text'])
        self.assertTrue(mock_send_bulk_sms.delay.called_once_with(ANY, ANY, self.poll_to_send['text']))

        retrieved_poll = Poll.objects(**self.poll_to_post)
        self.assertEqual(1, retrieved_poll.count())
        self.assertTrue(retrieved_poll[0].is_yesno_poll())

    @patch('dms.tasks.send_bulk_sms.delay')
    def test_should_post_to_all_contacts_in_sub_counties_under_district(self, mock_send_bulk_sms):
        poll_to_post_payload = self.poll_to_post.copy()
        poll_to_post_payload['target_locations'] = [str(self.kampala.id)]
        self.client.post(self.POLL_ENDPOINT, data=json.dumps(self.poll_to_post), content_type="application/json")
        mock_send_bulk_sms.assert_called_with(ANY, [u'+250775019449', u'+4343245552'], ANY)

    @patch('dms.tasks.send_bulk_sms.delay')
    def test_should_post_to_all_contacts_in_sub_counties(self, mock_send_bulk_sms):
        poll_to_post_payload = self.poll_to_post.copy()
        poll_to_post_payload['target_locations'] = [str(self.bukoto.id)]
        self.client.post(self.POLL_ENDPOINT, data=json.dumps(self.poll_to_post), content_type="application/json")
        mock_send_bulk_sms.assert_called_with(ANY, [u'+250775019449', u'+4343245552'], ANY)

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

    def test_should_not_get_a_list_of_polls_if_unauthorized(self):
        self.client.logout()
        self.assert_permission_required_for_get(self.POLL_ENDPOINT)
        self.assert_permission_required_for_post(self.POLL_ENDPOINT)


    def test_ddmc_should_get_a_list_of_polls_of_his_district(self):
        self.client.logout()
        user = self.login_user_with_group(self.ddmc_group)
        user_attr = dict(name='sam', phone='+256775019441', location=self.amuru, email=None, user=user)
        UserProfile(**(user_attr)).save()
        poll = Poll(**self.poll_to_post).save()
        poll2 = Poll(**self.poll_to_post2).save()

        response = self.client.get(self.POLL_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(poll2.target_locations, response.data[0]['target_locations'])
        self.assertEqual(poll2.target_locations[0], response.data[0]['target_locations'][0])
        self.assertNotEqual(poll.target_locations[0], response.data[0]['target_locations'][0])

    def test_should_get_a_list_of_polls_with_only_view_permissions(self):
        endpoint = self.POLL_ENDPOINT
        self.login_with_permission('can_view_polls')
        response = self.client.get(endpoint)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(endpoint)
        self.assertEquals(response.status_code, 403)


    @patch('dms.tasks.send_bulk_sms')
    @override_settings(ALWAYS_OPEN_POLLS=1)
    def test_should_auto_close_polls(self, mock_send_bulk_sms):
        self.poll_to_post['question'] = 'Will you comply, yes or no?'
        self.poll_to_post['ptype'] = 'yesno'
        second_poll = self.poll_to_post.copy()
        second_poll['question'] = 'Please say, yes or no?'
        second_poll['keyword'] = 'anotherkey'
        # self.poll_to_send['text'] = 'Will you comply, yes or no? Reply With: NECOCPoll YES/NO'

        response = self.client.post(self.POLL_ENDPOINT, data=json.dumps(self.poll_to_post),
                                    content_type="application/json")
        self.assertEqual(201, response.status_code)
        retrieved_poll = Poll.objects(**self.poll_to_post)
        self.assertEqual(1, retrieved_poll.count())
        self.assertEqual(True, retrieved_poll[0].open)

        response = self.client.post(self.POLL_ENDPOINT, data=json.dumps(second_poll),
                                    content_type="application/json")
        self.assertEqual(201, response.status_code)
        retrieved_poll = Poll.objects(**self.poll_to_post)
        self.assertEqual(1, retrieved_poll.count())
        self.assertEqual(False, retrieved_poll[0].open)

        retrieved_poll = Poll.objects(**second_poll)
        self.assertEqual(1, retrieved_poll.count())
        self.assertEqual(True, retrieved_poll[0].open)




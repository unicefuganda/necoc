import datetime
from django.test import override_settings
from dms.models import Poll

from dms.models.location import Location
from dms.models.user_profile import UserProfile
from dms.models.poll_response import PollResponse, ResponseCategory, PollResponseCategory
from dms.tests.base import MongoTestCase


class PollResponseTest(MongoTestCase):

    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "256775019449"

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='subcounty')).save()
        self.mobile_user = UserProfile(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()

        self.poll_response = dict(phone_no=phone_number, text="NECOC There is a fire", received_at=date_time, relayer_id=234,
                        run_id=23243)

        self.poll_attr = dict(name="Disaster", question="How many disasters are in your area?", keyword="some_word",
                         target_locations=[str(self.village.id)])
        self.poll = Poll(**self.poll_attr).save()

    def test_fields(self):
        expected_fields = ['text', 'created_at', 'phone_no', 'received_at', 'location', 'poll']
        rapidpro_message = PollResponse()
        for field in expected_fields:
            self.assertTrue(hasattr(rapidpro_message, field))

    def test_save_poll_response(self):
        self.poll_response['poll'] = self.poll

        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

    def test_poll_response_source(self):
        poll_response = PollResponse(**self.poll_response)

        self.assertEqual('NECOC Volunteer', poll_response.source())

    def test_poll_response_knows_its_mobile_user(self):
        poll_response = PollResponse(**self.poll_response)

        self.assertEqual(self.mobile_user, poll_response.mobile_user())

    def test_poll_response_gets_the_location_of_its_responder(self):
        rapid_pro_poll_response = PollResponse(**self.poll_response).save()
        self.assertEqual(self.village, rapid_pro_poll_response.location)

    def test_response_location_is_none_if_mobile_user_not_registered(self):
        some_non_registered_number = '1234'
        self.poll_response['phone_no'] = some_non_registered_number
        poll_response = PollResponse(**self.poll_response).save()
        self.assertIsNone(poll_response.location)

    @override_settings(POLL_RESPONSE_KEYWORD_INDEX=3)
    def test_responses_with_keyword_is_automatically_associated_to_poll(self):
        poll_response_attr = self.poll_response.copy()
        poll_response_attr['text'] = "NECOCPoll haha %s she no want designer" % self.poll.keyword

        self.assertNotIn('poll', poll_response_attr.keys())

        poll_response = PollResponse(**poll_response_attr).save()

        self.assertEqual(self.poll, poll_response.poll)

    @override_settings(POLL_RESPONSE_KEYWORD_INDEX=2)
    def test_responses_with_no_matching_keyword_does_not_get_poll(self):
        poll_response_attr = self.poll_response.copy()
        poll_response_attr['text'] = "NECOCPoll not_keyword haha she no want designer"

        self.assertNotIn('poll', poll_response_attr.keys())

        poll_response = PollResponse(**poll_response_attr).save()

        self.assertIsNone(poll_response.poll)

    @override_settings(POLL_RESPONSE_KEYWORD_INDEX=2)
    def test_responses_with_misplaced_keywords_get_assigned_poll(self):
        poll_response_attr = self.poll_response.copy()
        poll_response_attr['text'] = "NECOCPoll haha she no want %s designer" % self.poll.keyword

        self.assertNotIn('poll', poll_response_attr.keys())

        poll_response = PollResponse(**poll_response_attr).save()

        self.assertIsNotNone(poll_response.poll)
        self.assertEqual(self.poll, poll_response.poll)

    @override_settings(POLL_RESPONSE_KEYWORD_INDEX=3)
    def test_responses_get_both_poll_and_location(self):
        poll_response_attr = self.poll_response.copy()
        poll_response_attr['text'] = "NECOCPoll haha %s she no want designer" % self.poll.keyword

        poll_response = PollResponse(**poll_response_attr).save()

        self.assertEqual(self.poll, poll_response.poll)
        self.assertEqual(self.village, poll_response.location)
        self.assertEqual('Kampala >> Bukoto', poll_response.location_str())

    def test_should_process_and_categorise_yesno_poll_responses(self):
        self.poll_attr['ptype'] = 'yesno'
        self.poll_attr['keyword']  = 'akeyword'
        poll = Poll(**self.poll_attr).save()

        self.poll_response['text'] = 'yes'
        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

        yes_category = ResponseCategory.objects(**dict(poll=poll, name='yes')).first()

        self.assertEqual(1, PollResponseCategory.objects.count())
        self.assertEqual(1, PollResponseCategory.objects(**dict(response_category=yes_category, poll_response=poll_response.first())).count())

        #a 'NO' Response
        self.poll_response['text'] = 'nah'
        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

        no_category = ResponseCategory.objects(**dict(poll=poll, name='no')).first()

        self.assertEqual(2, PollResponseCategory.objects.count())
        self.assertEqual(1, PollResponseCategory.objects(**dict(response_category=no_category, poll_response=poll_response.first())).count())

        #a 'unknown' Response
        self.poll_response['text'] = 'very wiered response'
        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

        unknown_category = ResponseCategory.objects(**dict(poll=poll, name='unknown')).first()

        self.assertEqual(3, PollResponseCategory.objects.count()) #bad response not associated with poll
        self.assertEqual(1, PollResponseCategory.objects(**dict(response_category=unknown_category, poll_response=poll_response.first())).count())

        #should count results
        results_count = poll.yesno_poll_stats()
        self.assertEqual(1, results_count['yes'])
        self.assertEqual(1, results_count['unknown'])
        self.assertEqual(1, results_count['no'])

    def test_should_process_and_categorise_yesno_poll_responses_with_starting_keyword(self):
        self.poll_attr['ptype'] = 'yesno'
        self.poll_attr['keyword']  = 'akeyword'
        poll = Poll(**self.poll_attr).save()

        self.poll_response['text'] = 'NECOCPoll yes'
        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

        yes_category = ResponseCategory.objects(**dict(poll=poll, name='yes')).first()

        self.assertEqual(1, PollResponseCategory.objects.count())
        self.assertEqual(1, PollResponseCategory.objects(**dict(response_category=yes_category, poll_response=poll_response.first())).count())

        #a 'NO' Response
        self.poll_response['text'] = 'NECOCPoll.nah'
        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

        no_category = ResponseCategory.objects(**dict(poll=poll, name='no')).first()

        self.assertEqual(2, PollResponseCategory.objects.count())
        self.assertEqual(1, PollResponseCategory.objects(**dict(response_category=no_category, poll_response=poll_response.first())).count())

        #a 'unknown' Response
        self.poll_response['text'] = 'NECOCPoll very wiered response'
        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

        unknown_category = ResponseCategory.objects(**dict(poll=poll, name='unknown')).first()

        self.assertEqual(3, PollResponseCategory.objects.count()) #bad response not associated with poll
        self.assertEqual(1, PollResponseCategory.objects(**dict(response_category=unknown_category, poll_response=poll_response.first())).count())

    def test_should_process_and_categorise_yesno_poll_responses_when_yesno_is_misplaced(self):
        self.poll_attr['ptype'] = 'yesno'
        self.poll_attr['keyword']  = 'akeyword'
        poll = Poll(**self.poll_attr).save()

        self.poll_response['text'] = 'NECOCPoll a very bad yes answer'
        PollResponse(**self.poll_response).save()

        poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, poll_response.count())

        yes_category = ResponseCategory.objects(**dict(poll=poll, name='yes')).first()

        self.assertEqual(1, PollResponseCategory.objects.count())
        self.assertEqual(1, PollResponseCategory.objects(**dict(response_category=yes_category, poll_response=poll_response.first())).count())



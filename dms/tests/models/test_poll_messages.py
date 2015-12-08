import time
from django.test.utils import override_settings
from mongoengine import NotUniqueError, ValidationError
from dms.models import Location, PollResponse, ResponseCategory, UserProfile
from dms.models.poll import Poll, Rule
from dms.tests.base import MongoTestCase


class TestPoll(MongoTestCase):

    def setUp(self):
        self.phone_number = "256775019449"

        kampala = Location(**dict(name='Kampala', parent=None, type='district')).save()
        gulu = Location(**dict(name='Gulu', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=kampala, type='subcounty')).save()
        self.mobile_user = UserProfile(**dict(name='timothy', phone=self.phone_number, location=self.village, email=None)).save()
        self.mobile_user2 = UserProfile(**dict(name='mobile_user2', phone='256775019441', location=self.village, email=None)).save()
        self.mobile_user3 = UserProfile(**dict(name='mobile_user3', phone='256775019442', location=gulu, email=None)).save()
        self.mobile_user4 = UserProfile(**dict(name='mobile_user4', phone='256775019443', location=kampala, email=None)).save()

        self.target_locations = [str(kampala.id), str(gulu.id)]
        self.poll = dict(name="Disaster", question="How many disasters are in your area?", keyword="some word",
                         target_locations=self.target_locations)

    def test_save_poll(self):
        Poll(**self.poll).save()
        polls = Poll.objects(**self.poll)
        self.assertEqual(1, polls.count())

        poll = polls.first()
        self.assertIn(self.target_locations[0], poll.target_locations)
        self.assertIn(self.target_locations[1], poll.target_locations)

    def test_should_not_save_a_poll_if_key_is_not_unique(self):
        Poll(**self.poll).save()
        self.assertRaises(NotUniqueError, Poll(**self.poll).save)

    def test_should_not_save_a_poll_if_keyword_is_more_than_10_characters(self):
        self.poll['keyword'] = "l"*11
        self.assertRaises(ValidationError, Poll(**self.poll).save)

    def test_should_not_save_a_poll_if_question_is_more_than_160_characters(self):
        self.poll['question'] = "l"*161
        self.assertRaises(ValidationError, Poll(**self.poll).save)

    def test_should_know_its_number_of_responses(self):
        poll = Poll(**self.poll).save()
        poll_response_attr = dict(phone_no='123455', text="NECOC There is a fire", relayer_id=234,
                        run_id=23243, poll=poll)

        poll_response = PollResponse(**poll_response_attr).save()

        self.assertEqual(1, poll.number_of_responses())
        self.assertIn(poll_response, poll.responses())


    @override_settings(STARTSWITH_PATTERN_TEMPLATE='some%sregex')
    @override_settings(YES_WORDS=['YES', 'Yeah'])
    @override_settings(NO_WORDS=['No', 'NAh'])
    def test_should_save_yesno_poll_with_default_yesno_categories(self):
        self.poll['ptype'] = 'yesno'
        poll = Poll(**self.poll).save()

        self.assertEqual(1, Poll.objects.count())
        self.assertEqual(True, poll.is_yesno_poll())

        yes_category = ResponseCategory.objects(**dict(poll=poll, name='yes')).first()
        no_category = ResponseCategory.objects(**dict(poll=poll, name='no')).first()
        self.assertEqual(2, Rule.objects.count())
        self.assertEqual(u'someYES|Yeahregex', Rule.objects(**dict(response_category=yes_category)).first().regex)
        self.assertEqual(u'someNo|NAhregex', Rule.objects(**dict(response_category=no_category)).first().regex)

    @override_settings(ALWAYS_OPEN_POLLS=2)
    def test_should_auto_close_old_polls(self):
        keywords = ['someword', 'otherkey', 'another']
        for kw in keywords:
            self.poll['keyword'] = kw
            Poll(**self.poll).save()
            time.sleep(1)

        self.assertEqual(3, Poll.objects.count())
        self.assertEqual(2, Poll.objects(open=True).count())
        self.assertEqual(1, Poll.objects(open=False).count())
        self.assertEqual(True, Poll.objects(keyword='otherkey').first().open)
        self.assertEqual(True, Poll.objects(keyword='another').first().open)
        self.assertEqual(False, Poll.objects(keyword='someword').first().open)

    def test_should_know_its_number_of_participants(self):
        poll = Poll(**self.poll).save()

        self.assertEqual(4, poll.number_of_participants())

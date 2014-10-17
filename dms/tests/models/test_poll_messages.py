from mongoengine import NotUniqueError, ValidationError
from dms.models import Location
from dms.models.poll import Poll
from dms.tests.base import MongoTestCase


class TestPoll(MongoTestCase):

    def setUp(self):
        kampala = Location(**dict(name='Kampala', parent=None, type='district')).save()
        gulu = Location(**dict(name='Gulu', parent=None, type='district')).save()

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
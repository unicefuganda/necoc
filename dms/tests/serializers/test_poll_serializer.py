from dms.api.poll_endpoint import PollSerializer
from dms.models import Poll, Location
from dms.tests.base import MongoTestCase


class PollSerializerTest(MongoTestCase):

    def setUp(self):
        kampala = Location(**dict(name='Kampala', parent=None, type='district')).save()
        gulu = Location(**dict(name='Gulu', parent=None, type='district')).save()
        self.target_locations = [str(kampala.id), str(gulu.id)]
        self.poll = dict(name="Disaster", question="How many disasters are in your area?", keyword="some word",
                         target_locations=self.target_locations)
        self.serialized_poll = dict(name=u'Disaster', question=u'How many disasters are in your area?',
                                    keyword=u'some word', target_locations=self.target_locations)

    def test_should_serialize_poll_object(self):
        poll = Poll(**self.poll).save()
        serialized_object = PollSerializer(poll)

        self.assertDictContainsSubset(self.serialized_poll, serialized_object.data)
        self.assertIsNotNone(serialized_object.data['id'])

    def test_should_deserialize_location_object(self):
        serializer = PollSerializer(data=self.serialized_poll)

        self.assertTrue(serializer.is_valid())
        saved_poll = serializer.save()

        self.assertTrue(isinstance(saved_poll, Poll))
        for attribute, value in self.poll.items():
            self.assertEqual(value, getattr(saved_poll, attribute))
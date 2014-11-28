from dms.api.poll_endpoint import PollSerializer
from dms.api.poll_response_endpoint import PollResponseSerializer
from dms.models import Poll
from dms.models.location import Location
from dms.models.user_profile import UserProfile
from dms.models.poll_response import PollResponse
from dms.tests.base import MongoTestCase
import datetime


class PollResponseSerializerTest(MongoTestCase):
    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "256775019449"
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = UserProfile(
            **dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()


        self.poll_attr = dict(name="Disaster", question="How many disasters are in your area?", keyword="some_word",
                         target_locations=[str(self.village.id)])
        self.poll = Poll(**self.poll_attr).save()

        self.text_format = "NECOCPoll %s there are 4 or 5"
        text = self.text_format % self.poll_attr['keyword']

        self.poll_response = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234,
                            run_id=23243)
        self.serialized_data = dict(phone=phone_number, time=date_time, relayer=234, run=23243,
                            text=text)

    def test_should_serialize_poll_response_object(self):
        poll_response = PollResponse(**self.poll_response).save()
        serialized_object = PollResponseSerializer(poll_response)
        serialized_poll = PollSerializer(self.poll)
        serialized_data_with_source = dict(self.serialized_data.items() +
                                           {'id': str(poll_response.id), 'source': 'NECOC Volunteer',
                                            'poll': serialized_poll.data, 'location': 'Kampala >> Bukoto'}.items())

        expected_response_fields = ['text', 'relayer', 'phone', 'time', 'location', 'run', 'id']
        expected_poll_fields = ['name', 'keyword', 'question', 'id', 'target_locations']

        for field in expected_response_fields:
            self.assertEqual(serialized_data_with_source[field], serialized_object.data[field])

        for field in expected_poll_fields:
            self.assertEqual(serialized_data_with_source['poll'][field], serialized_object.data['poll'][field])

    def test_should_deserialize_poll_response_object(self):
        serializer = PollResponseSerializer(data=self.serialized_data)

        self.assertTrue(serializer.is_valid())

        saved_message = serializer.save()

        self.assertTrue(isinstance(saved_message, PollResponse))
        for attribute, value in self.poll_response.items():
            self.assertEqual(value, getattr(saved_message, attribute))
import datetime
from dms.models import Location, MobileUser, Poll
from dms.models.poll_response import PollResponse
from dms.tests.base import MongoAPITestCase


class PollResponseEndPointTest(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/poll-responses/'

    def setUp(self):
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = MobileUser(**dict(name='timothy', phone="+256775019449",
                                             location=self.village, email=None)).save()

        self.poll_attr = dict(name="Disaster", question="How many disasters are in your area?", keyword="some_word",
                         target_locations=[str(self.village.id)])
        self.poll = Poll(**self.poll_attr).save()


        self.text_format = "NECOCPoll %s there are 4 or 5"
        text = self.text_format % self.poll_attr['keyword']
        self.expected_poll_response = dict(phone="+256775019449", text=text, time=self.date_time, relayer=234,
                                     run=23243)
        self.poll_response = dict(phone_no="+256775019449", text=text, received_at=self.date_time,
                            relayer_id=234, run_id=23243)

    def _api_url(self, id):
        return "%s%s/" % (self.API_ENDPOINT, str(id))

    def test_should_create_rapid_pro_poll_response(self):
        response = self.client.post(self.API_ENDPOINT, data=self.expected_poll_response)
        self.assertEqual(201, response.status_code)

        retrieved_poll_response = PollResponse.objects(**self.poll_response)
        self.assertEqual(1, retrieved_poll_response.count())

    def test_should_get_rapid_pro_poll_response(self):
        PollResponse(**self.poll_response).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.expected_poll_response, response.data[0])
        self.assertEqual('NECOC Volunteer', response.data[0]['source'])
        self.assertEqual('Kampala >> Bukoto', response.data[0]['location'])
        self.assertIsNotNone(response.data[0]['id'])

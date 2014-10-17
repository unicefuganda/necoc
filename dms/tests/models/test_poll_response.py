import datetime

from dms.models.location import Location
from dms.models.mobile_user import MobileUser
from dms.models.poll_response import PollResponse
from dms.tests.base import MongoTestCase


class PollResponseTest(MongoTestCase):

    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = MobileUser(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()
        
        self.poll_response = dict(phone_no=phone_number, text="NECOC There is a fire", received_at=date_time, relayer_id=234,
                        run_id=23243)

    def test_save_poll_response(self):

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
        poll_response_location = rapid_pro_poll_response.location
        self.assertEqual(self.village, poll_response_location)
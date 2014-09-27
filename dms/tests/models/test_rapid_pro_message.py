import datetime
from dms.models.location import Location
from dms.models.mobile_user import MobileUser

from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoTestCase


class TestRapidProMessage(MongoTestCase):

    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text="There is a fire", received_at=date_time, relayer_id=234,
                        run_id=23243)

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = MobileUser(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()

    def test_save_rapid_pro_message(self):

        RapidProMessage(**self.message).save()
        rp_messages = RapidProMessage.objects(**self.message)
        self.assertEqual(1, rp_messages.count())

    def test_message_source(self):
        rapid_pro_message = RapidProMessage(**self.message)

        self.assertEqual('NECOC Volunteer', rapid_pro_message.source())

    def test_message_knows_its_mobile_user(self):
        rapid_pro_message = RapidProMessage(**self.message)

        self.assertEqual(self.mobile_user, rapid_pro_message.mobile_user())

    def test_message_knows_the_location_of_where_it_was_reported_from(self):
        rapid_pro_message = RapidProMessage(**self.message)

        message_location = rapid_pro_message.location()

        self.assertEqual(self.village, message_location)

    def test_message_location_is_none_if_mobile_user_not_registered(self):
        some_non_registered_number = '1234'
        self.message['phone_no'] = some_non_registered_number
        rapid_pro_message = RapidProMessage(**self.message)

        message_location = rapid_pro_message.location()

        self.assertIsNone(message_location)

    def test_message_location_str_returns_the_to_str_of_its_location(self):
        rapid_pro_message = RapidProMessage(**self.message)
        message_location_str = rapid_pro_message.location_str()

        self.assertEqual("Kampala >> Bukoto", message_location_str)

    def test_message_location_str_is_empty_if_no_location(self):
        new_phone_no_without_location = '1234'
        self.message['phone_no'] = new_phone_no_without_location
        rapid_pro_message = RapidProMessage(**self.message)
        message_location_str = rapid_pro_message.location_str()

        self.assertEqual("", message_location_str)


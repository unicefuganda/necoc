import datetime
from django.test import override_settings

from dms.models.location import Location
from dms.models.user_profile import UserProfile
from dms.models.rapid_pro_message import RapidProMessageBase
from dms.tests.base import MongoTestCase


class TestRapidProMessageBase(MongoTestCase):

    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "256775019449"

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = UserProfile(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()
        
        self.message = dict(phone_no=phone_number, text="NECOC There is a fire", received_at=date_time, relayer_id=234,
                        run_id=23243)

    def test_fields(self):
        expected_fields = ['text', 'created_at', 'phone_no', 'received_at', 'location']
        rapidpro_message = RapidProMessageBase()
        for field in expected_fields:
            self.assertTrue(hasattr(rapidpro_message, field))

    def test_save_rapid_pro_message(self):

        RapidProMessageBase(**self.message).save()
        rp_messages = RapidProMessageBase.objects(**self.message)
        self.assertEqual(1, rp_messages.count())

    def test_message_source(self):
        rapid_pro_message = RapidProMessageBase(**self.message)

        self.assertEqual('NECOC Volunteer', rapid_pro_message.source())

    def test_message_knows_its_mobile_user(self):
        rapid_pro_message = RapidProMessageBase(**self.message)

        self.assertEqual(self.mobile_user, rapid_pro_message.mobile_user())

    @override_settings(INTERNATIONAL_PHONE_PREFIX='00')
    def test_international_sign_is_stripped_from_phone_number_to_identify_mobile_user(self):
        message_attr = self.message.copy()
        message_attr['phone_no'] = '00' + self.mobile_user.phone
        rapid_pro_message = RapidProMessageBase(**message_attr)

        self.assertEqual(self.mobile_user, rapid_pro_message.mobile_user())

    def test_message_location_str_returns_the_to_str_of_its_location(self):
        message = self.message.copy()
        message['location'] = self.village

        rapid_pro_message = RapidProMessageBase(**message).save()

        self.assertEqual("Kampala >> Bukoto", rapid_pro_message.location_str())

    def test_message_location_str_is_empty_if_no_location(self):
        rapid_pro_message = RapidProMessageBase(**self.message).save()

        self.assertEqual("", rapid_pro_message.location_str())

    def test_get_messages_from_a_location(self):
        location_name = 'Abim'
        district = Location(**dict(name=location_name, parent=None, type='district')).save()
        message_attr = self.message.copy()
        message_attr['location'] = district
        message = RapidProMessageBase(**message_attr).save()
        message1 = RapidProMessageBase(**self.message).save()

        location_messages = RapidProMessageBase.from_(district)

        self.assertEqual(1, location_messages.count())
        self.assertIn(message, location_messages)
        self.assertNotIn(message1, location_messages)

    def test_get_messages_given_from_date_and_to_date(self):
        location_name = 'Abim'
        district = Location(**dict(name=location_name, parent=None, type='district')).save()
        message_attr = self.message.copy()
        message_attr['location'] = district
        message_attr['received_at'] = datetime.datetime(2014, 12, 17, 16, 0, 49, 807000)
        message = RapidProMessageBase(**message_attr).save()

        self.message['location'] = district
        message1 = RapidProMessageBase(**self.message).save()

        location_messages = RapidProMessageBase.from_(district, **{'from': '2014-09-17', 'to': '2014-10-17'})

        self.assertEqual(1, location_messages.count())
        self.assertIn(message1, location_messages)
        self.assertNotIn(message, location_messages)

        location_messages = RapidProMessageBase.from_(district, **{'from': None, 'to': None})
        self.assertEqual(2, location_messages.count())

    def test_get_message_count_given_from_and_to_date(self):
        message_attr = self.message.copy()
        message_attr['received_at'] = datetime.datetime(2014, 11, 17, 16, 0, 49, 807000)
        RapidProMessageBase(**message_attr).save()
        RapidProMessageBase(**self.message).save()

        location_messages_count = RapidProMessageBase.count_(**{'from': '2014-09-17', 'to': '2014-10-17'})
        self.assertEqual(1, location_messages_count)

        location_messages_count = RapidProMessageBase.count_(**{'from': '2014-08-17', 'to': '2014-12-17'})
        self.assertEqual(2, location_messages_count)

        location_messages_count = RapidProMessageBase.count_(**{'from': '2014-08-17'})
        self.assertEqual(2, location_messages_count)

        location_messages_count = RapidProMessageBase.count_(**{'from': None, 'to': None})
        self.assertEqual(2, location_messages_count)

    def test_get_messages_from_children_are_also_added(self):
        location_name = 'Abim'
        district = Location(**dict(name=location_name, parent=None, type='district')).save()
        message_attr = self.message.copy()
        message_attr['location'] = district
        message = RapidProMessageBase(**message_attr).save()

        message1_attr = message_attr.copy()
        location_name = 'Wakiso'
        district_son = Location(**dict(name=location_name, parent=district, type='village')).save()
        message1_attr["location"] = district_son
        message1 = RapidProMessageBase(**message1_attr).save()

        location_messages = RapidProMessageBase.from_(district)

        self.assertEqual(2, location_messages.count())
        self.assertIn(message, location_messages)
        self.assertIn(message1, location_messages)

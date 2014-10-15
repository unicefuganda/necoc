import datetime
from django.test import override_settings
from dms.models.location import Location
from dms.models.mobile_user import MobileUser

from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoTestCase


class TestRapidProMessage(MongoTestCase):

    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = MobileUser(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()
        
        self.message = dict(phone_no=phone_number, text="NECOC There is a fire", received_at=date_time, relayer_id=234,
                        run_id=23243)

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

    @override_settings(MESSAGE_LOCATION_INDEX=3)
    def test_message_gets_the_location_if_it_is_militarily_coded_and_matched(self):
        message = self.message.copy()
        message['text'] = "NECOC Fire Kampala"
        rapid_pro_message = RapidProMessage(**message)

        message_location = rapid_pro_message.location

        self.assertEqual(self.district, message_location)

    @override_settings(MESSAGE_LOCATION_INDEX=2)
    def test_message_has_no_location_if_message_content_does_not_specify_location(self):
        message = self.message.copy()
        message['text'] = "NECOC hahaha Fire"
        rapid_pro_message = RapidProMessage(**message)

        self.assertIsNone(rapid_pro_message.location)

    def test_message_location_str_returns_the_to_str_of_its_location(self):
        message = self.message.copy()
        message['text'] = "NECOC Bukoto there are some serious fire over here"

        rapid_pro_message = RapidProMessage(**message)

        self.assertEqual("Kampala >> Bukoto", rapid_pro_message.location_str())

    def test_message_location_str_is_empty_if_no_location(self):
        message = self.message.copy()
        message['text'] = "NECOC UnknownLocation there are some serious fire over here"

        rapid_pro_message = RapidProMessage(**message)

        self.assertEqual("", rapid_pro_message.location_str())

    def test_get_messages_from_a_location(self):
        location_name = 'Abim'
        text = "NECOC %s fire baba fire" % location_name
        district = Location(**dict(name=location_name, parent=None, type='district')).save()
        message_attr = self.message.copy()
        message_attr['text'] = text
        message = RapidProMessage(**message_attr).save()

        message1_attr = message_attr.copy()
        message1_attr["text"] = " message without location"
        message1 = RapidProMessage(**message1_attr).save()

        location_messages = RapidProMessage.from_(district)

        self.assertEqual(1, location_messages.count())
        self.assertIn(message, location_messages)
        self.assertNotIn(message1, location_messages)


    def test_get_messages_from_children_are_also_added(self):
        location_name = 'Abim'
        text = "NECOC %s fire baba fire" % location_name
        district = Location(**dict(name=location_name, parent=None, type='district')).save()
        message_attr = self.message.copy()
        message_attr['text'] = text
        message = RapidProMessage(**message_attr).save()

        message1_attr = message_attr.copy()
        location_name = 'Wakiso'
        text = "NECOC %s fire baba fire" % location_name
        district_son = Location(**dict(name=location_name, parent=district, type='village')).save()
        message1_attr["text"] = text
        message1 = RapidProMessage(**message1_attr).save()

        location_messages = RapidProMessage.from_(district)

        self.assertEqual(2, location_messages.count())
        self.assertIn(message, location_messages)
        self.assertIn(message1, location_messages)


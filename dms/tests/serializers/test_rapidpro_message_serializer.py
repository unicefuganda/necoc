import pytz
from dms.api.rapid_pro_endpoint import RapidProMessageSerializer
from dms.models import DisasterType, Disaster, AdminSetting
from dms.models.location import Location
from dms.models.user_profile import UserProfile
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoTestCase
import datetime


class RapidProMessageSerializerTest(MongoTestCase):
    def setUp(self):
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = UserProfile(
            **dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()
        text = "NECOC.%s. There is a fire" % self.village.name
        self.message = dict(phone_no=phone_number, text=text, received_at=self.date_time, relayer_id=234,
                            run_id=23243)
        self.serialized_data = dict(phone=phone_number, time=self.date_time, relayer=234, run=23243,
                            text=text)
        AdminSetting(**dict(name='enable_volunteer_profiles')).save()

    def test_should_serialize_rapid_pro_message_object(self):
        rapid_pro_message = RapidProMessage(**self.message).save()
        serialized_object = RapidProMessageSerializer(rapid_pro_message)
        self.serialized_data['time'] = self.date_time.replace(tzinfo=pytz.utc)
        serialized_data_with_source = dict(self.serialized_data.items() +
                                           {'id': str(rapid_pro_message.id),
                                            'source': self.mobile_user.name,
                                            'disaster': None,
                                            'location': 'Kampala >> Bukoto',
                                            'profile_id':str(self.mobile_user.id),
                                            'auto_associated': False}.items())
        self.assertEqual(serialized_data_with_source, serialized_object.data)

    def test_should_deserialize_rapid_pro_message_object(self):
        serializer = RapidProMessageSerializer(data=self.serialized_data)

        self.assertTrue(serializer.is_valid())

        saved_message = serializer.save()

        self.assertTrue(isinstance(saved_message, RapidProMessage))
        for attribute, value in self.message.items():
            self.assertEqual(value, getattr(saved_message, attribute))

    def test_editing_existing_message_is_valid(self):
        district = Location(**dict(name='Kampala', type='district', parent=None)).save()
        disaster_type = DisasterType(**dict(name="Fire", description="Fire")).save()

        disaster_attributes = dict(name=disaster_type, locations=[district],
                             description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")
        disaster = Disaster(**disaster_attributes).save()

        message = RapidProMessage(**self.serialized_data).save()

        data = self.serialized_data.copy()
        data['disaster'] = disaster.id

        serializer = RapidProMessageSerializer(message, data=data)

        self.assertTrue(serializer.is_valid())
        new_message = serializer.save()

        self.assertTrue(message.id, new_message.id)
        self.assertEqual(disaster, new_message.disaster)

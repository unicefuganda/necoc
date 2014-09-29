from dms.api.rapid_pro_endpoint import RapidProMessageSerializer
from dms.models.location import Location
from dms.models.mobile_user import MobileUser
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoTestCase
import datetime


class RapidProMessageSerializerTest(MongoTestCase):
    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.serialized_data = dict(phone=phone_number, time=date_time, relayer=234, run=23243,
                                    text="There is a fire")

        self.message = dict(phone_no=phone_number, text="There is a fire", received_at=date_time, relayer_id=234,
                            run_id=23243)

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = MobileUser(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()

    def test_should_serialize_rapid_pro_message_object(self):

        rapid_pro_message = RapidProMessage(**self.message).save()
        serialized_object = RapidProMessageSerializer(rapid_pro_message)
        serialized_data_with_source = dict(self.serialized_data.items() +
                                           {'source': 'NECOC Volunteer', 'location': 'Kampala >> Bukoto'}.items())
        self.assertEqual(serialized_data_with_source, serialized_object.data)

    def test_should_deserialize_rapid_pro_message_object(self):
        serializer = RapidProMessageSerializer(data=self.serialized_data)

        self.assertTrue(serializer.is_valid())

        saved_message = serializer.save()

        self.assertTrue(isinstance(saved_message, RapidProMessage))
        for attribute, value in self.message.items():
            self.assertEqual(value, getattr(saved_message, attribute))

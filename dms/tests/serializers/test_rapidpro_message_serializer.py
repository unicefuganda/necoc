from dms.api.rapid_pro_message import RapidProMessageSerializer
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoTestCase
import datetime


class RapidProMessageSerializerTest(MongoTestCase):
    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.serialized_data = dict(phone="+256775019449", time=date_time, relayer=234, sms=23243,
                                    text="There is a fire", relayer_phone="+256773434324", status="Q",
                                    direction="I", event="mo_sms")

        self.message = dict(phone_no="+256775019449", text="There is a fire", received_at=date_time, relayer_id=234,
                            relayer_phone="+256773434324", sms_id=23243, status="Q", direction="I", event="mo_sms")

    def tearDown(self):
        RapidProMessage.drop_collection()

    def test_should_serialize_rapid_pro_message_object(self):
        rapid_pro_message = RapidProMessage(**self.message).save()
        serialized_object = RapidProMessageSerializer(rapid_pro_message)
        self.assertEqual(self.serialized_data, serialized_object.data)

    def test_should_deserialize_rapid_pro_message_object(self):
        serializer = RapidProMessageSerializer(data=self.serialized_data)

        self.assertTrue(serializer.is_valid())

        saved_message = serializer.save()

        self.assertTrue(isinstance(saved_message, RapidProMessage))
        for attribute, value in self.message.items():
            self.assertEqual(value, getattr(saved_message, attribute))

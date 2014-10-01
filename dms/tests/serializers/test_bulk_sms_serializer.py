from dms.api.bulk_sms_endpoint import SentMessageSerializer
from dms.models import SentMessage
from dms.tests.base import MongoTestCase


class BulkSMSSerializerTest(MongoTestCase):

    def setUp(self):
        phone_numbers = ["+256775019449", "2345"]
        self.serialized_sms = dict(phone_numbers=phone_numbers, text="There is a fire")
        self.sms = dict(phone_numbers=phone_numbers, text="There is a fire")

    def test_should_serialize_location_object(self):
        sms = SentMessage(**self.sms).save()
        serialized_object = SentMessageSerializer(sms)
        self.assertDictContainsSubset(self.serialized_sms, serialized_object.data)
        self.assertIsNotNone(serialized_object.data['id'])

    def test_should_deserialize_location_object(self):
        serializer = SentMessageSerializer(data=self.serialized_sms)

        self.assertTrue(serializer.is_valid())
        saved_sms = serializer.save()

        self.assertTrue(isinstance(saved_sms, SentMessage))
        for attribute, value in self.sms.items():
            self.assertEqual(value, getattr(saved_sms, attribute))
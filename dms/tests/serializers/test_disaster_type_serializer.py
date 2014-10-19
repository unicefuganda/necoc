from dms.api.disaster_type_endpoint import DisasterTypeSerializer
from dms.models import DisasterType
from dms.tests.base import MongoTestCase


class DisasterTypeSerializerTest(MongoTestCase):

    def setUp(self):
        self.serialized_disaster_type = dict(name="Fire", description="Fire")
        self.disaster_type = dict(name="Fire", description="Fire")

    def test_should_serialize_disaster_type_object(self):
        disaster_type = DisasterType(**self.disaster_type).save()
        serialized_object = DisasterTypeSerializer(disaster_type)
        self.assertDictContainsSubset(self.serialized_disaster_type, serialized_object.data)
        self.assertIsNotNone(serialized_object.data['id'])

    def test_should_deserialize_disaster_type_object(self):
        serializer = DisasterTypeSerializer(data=self.serialized_disaster_type)

        self.assertTrue(serializer.is_valid())
        saved_disaster_type = serializer.save()

        self.assertTrue(isinstance(saved_disaster_type, DisasterType))
        for attribute, value in self.disaster_type.items():
            self.assertEqual(value, getattr(saved_disaster_type, attribute))

    def test_serializer_should_be_invalid_when_deserializing_disaster_type_that_exists(self):
        serializer = DisasterTypeSerializer(data=self.serialized_disaster_type)
        serializer.is_valid()
        serializer.save()

        serializer = DisasterTypeSerializer(data=self.serialized_disaster_type)
        self.assertFalse(serializer.is_valid())

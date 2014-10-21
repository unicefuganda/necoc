from dms.api.location_endpoint import LocationSerializer
from dms.models.location import Location
from dms.tests.base import MongoTestCase


class LocationSerializerTest(MongoTestCase):
    def setUp(self):
        self.serialized_location = dict(name='Kampala', type='district', parent=None)
        self.location = dict(name='Kampala', type='district')

    def tearDown(self):
        Location.drop_collection()

    def test_should_serialize_location_object(self):
        location = Location(**self.location).save()
        serialized_object = LocationSerializer(location)
        self.assertDictContainsSubset(self.serialized_location, serialized_object.data)
        self.assertIsNotNone(serialized_object.data['id'])

    def test_should_deserialize_location_object(self):
        serializer = LocationSerializer(data=self.location)

        self.assertTrue(serializer.is_valid())
        saved_location = serializer.save()

        self.assertTrue(isinstance(saved_location, Location))
        for attribute, value in self.location.items():
            self.assertEqual(value, getattr(saved_location, attribute))

    def test_invalid_type_cannot_be_serialized(self):
        location_attr = self.location.copy()
        location_attr['type'] = 'invalid_type'

        serializer = LocationSerializer(data=location_attr)

        self.assertFalse(serializer.is_valid())

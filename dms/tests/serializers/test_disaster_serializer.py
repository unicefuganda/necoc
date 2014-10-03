import datetime
from dms.api.disaster_endpoint import DisasterSerializer
from dms.models import Location, DisasterType
from dms.models.disaster import Disaster
from dms.tests.base import MongoTestCase


class DisasterSerializerTest(MongoTestCase):
    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()

        self.disaster_type = DisasterType(**dict(name="Fire", description="Fire"))
        self.disaster_type.save()

        self.serialized_location = dict(created_at=self.district.created_at, type=self.district.type,
                                        name=self.district.name, id=str(self.district.id))

        self.serialized_disaster_type = dict(created_at=self.disaster_type.created_at, name=self.disaster_type.name,
                                             description=self.disaster_type.description, id=str(self.disaster_type.id))

        self.disaster = dict(name=self.disaster_type, location=self.district, description="Big Flood",
                             date=datetime.datetime(2014, 12, 1, 11, 3), status="Assessment")

        self.serialized_disaster = dict(name=self.serialized_disaster_type, location=self.serialized_location,
                                        description="Big Flood", date="2014-12-01T11:03", status="Assessment")

    def test_should_serialize_location_object(self):
        self.disaster['date'] = '2014-12-01'
        self.serialized_disaster['date'] = '2014-12-01'
        disaster = Disaster(**self.disaster).save()
        serialized_object = DisasterSerializer(disaster)
        self.assertDictContainsSubset(self.serialized_disaster, serialized_object.data)
        self.assertIsNotNone(serialized_object.data['id'])

    def test_should_deserialize_location_object(self):
        self.serialized_disaster['name'] = self.disaster_type.id
        self.serialized_disaster['location'] = self.district.id

        serializer = DisasterSerializer(data=self.serialized_disaster)
        self.assertTrue(serializer.is_valid())

        saved_disaster = serializer.save()
        self.assertTrue(isinstance(saved_disaster, Disaster))
        for attribute, value in self.disaster.items():
            self.assertEqual(value, getattr(saved_disaster, attribute))
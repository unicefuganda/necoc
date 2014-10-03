from dms.models import DisasterType
from dms.tests.base import MongoTestCase


class TestDisaster(MongoTestCase):
    def setUp(self):
        pass

    def test_create_disaster(self):
        attributes = {"name": "Flood", "description": "a lot of water everywhere"}
        DisasterType(**attributes).save()
        disasters = DisasterType.objects(name="Flood")
        disaster = disasters[0]

        self.assertEqual(1, disasters.count())
        self.assertEqual(attributes['name'], disaster.name)
        self.assertEqual(attributes['description'], disaster.description)

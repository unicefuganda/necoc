from dms.models.disaster import Disaster
from dms.tests.base import NoSQLTestCase


class TestDisaster(NoSQLTestCase):

    def setUp(self):
        pass

    def test_create_disaster(self):
        attributes = {"name": "Flood", "description":"a lot of water everywhere"}
        Disaster(**attributes).save()
        disasters = Disaster.objects(name="Flood")
        disaster = disasters[0]

        self.assertEqual(1, disasters.count())
        self.assertEqual(attributes['name'], disaster.name)
        self.assertEqual(attributes['description'], disaster.description)

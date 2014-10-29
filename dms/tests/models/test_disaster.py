from dms.models import DisasterType, Location
from dms.models.disaster import Disaster
from dms.tests.base import MongoTestCase


class TestDisasterModel(MongoTestCase):
    def setUp(self):
        self.disaster_type = DisasterType(**dict(name='Flood', description="Some flood"))
        self.disaster_type.save()

        self.district = Location(**dict(name='Kampala', type='district', parent=None)).save()

    def test_create_disaster(self):
        attributes = dict(name=self.disaster_type, locations=[self.district], description="Big Flood",
                          date="2014-12-01", status="Assessment")
        Disaster(**attributes).save()
        disasters = Disaster.objects(name=self.disaster_type, date="2014-12-01", status="Assessment")

        self.assertEqual(1, disasters.count())

    def test_get_messages_from_a_locations(self):
        attributes = dict(name=self.disaster_type, locations=[self.district], description="Big Flood",
                          date="2014-12-01", status="Assessment")
        disaster1 = Disaster(**attributes).save()

        attr2 = attributes.copy()
        attr2["locations"] = [Location(**dict(name='Some other location', type='district', parent=None)).save()]
        disaster2 = Disaster(**attr2).save()

        location_disasters = Disaster.from_(self.district)
        self.assertEqual(1, location_disasters.count())
        self.assertIn(disaster1, location_disasters)
        self.assertNotIn(disaster2, location_disasters)

    def test_get_messages_from_children_are_also_added(self):
        attributes = dict(name=self.disaster_type, locations=[self.district], description="Big Flood", date="2014-12-01",
                          status="Assessment")
        disaster1 = Disaster(**attributes).save()

        attr2 = attributes.copy()
        attr2["locations"] = [Location(**dict(name='Kampala subcounty', type='subcounty', parent=self.district)).save()]
        disaster2 = Disaster(**attr2).save()

        location_disasters = Disaster.from_(self.district)

        self.assertEqual(2, location_disasters.count())
        self.assertIn(disaster1, location_disasters)
        self.assertIn(disaster2, location_disasters)

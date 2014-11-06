import datetime
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

    def test_get_disaster_from_a_location(self):
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

    def test_get_disasters_given_from_date_and_to_date(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        attributes = dict(name=self.disaster_type, locations=[self.district], description="Big Flood",
                          date=date_time, status="Assessment")
        disaster1 = Disaster(**attributes).save()

        attr2 = attributes.copy()
        attr2["date"] = datetime.datetime(2014, 8, 17, 16, 0, 49, 807000)
        disaster2 = Disaster(**attr2).save()

        location_disasters = Disaster.from_(self.district, **dict(from_date='2014-08-17', to_date='2014-09-17'))
        self.assertEqual(1, location_disasters.count())
        self.assertIn(disaster2, location_disasters)
        self.assertNotIn(disaster1, location_disasters)

        location_disasters = Disaster.from_(self.district, **dict(from_date=None, to_date=None))
        self.assertEqual(2, location_disasters.count())

    def test_get_disaster_count_given_from_date_and_to_date(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        attributes = dict(name=self.disaster_type, locations=[self.district], description="Big Flood",
                          date=date_time, status="Assessment" )
        Disaster(**attributes).save()

        location_disasters = Disaster.count_(**dict(from_date='2014-08-17', to_date='2014-10-17'))
        self.assertEqual(1, location_disasters)

        location_disasters = Disaster.count_(**dict(from_date='2014-11-17', to_date='2014-12-17'))
        self.assertEqual(0, location_disasters)

        location_disasters = Disaster.count_(**dict(from_date=None, to_date=None))
        self.assertEqual(1, location_disasters)

    def test_get_messages_from_children_are_also_added(self):
        attributes = dict(name=self.disaster_type, locations=[self.district], description="Big Flood",
                          date="2014-12-01",
                          status="Assessment")
        disaster1 = Disaster(**attributes).save()

        attr2 = attributes.copy()
        attr2["locations"] = [Location(**dict(name='Kampala subcounty', type='subcounty', parent=self.district)).save()]
        disaster2 = Disaster(**attr2).save()

        location_disasters = Disaster.from_(self.district)

        self.assertEqual(2, location_disasters.count())
        self.assertIn(disaster1, location_disasters)
        self.assertIn(disaster2, location_disasters)

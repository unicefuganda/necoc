from dms.models import DisasterType, Location
from dms.models.disaster import Disaster
from dms.tests.base import MongoTestCase


class TestDisasterModel(MongoTestCase):
    def setUp(self):
        self.disaster_type = DisasterType(**dict(name='Flooad', description="Some flood"))
        self.disaster_type.save()

        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()

    def test_create_disaster(self):
        attributes = dict(name=self.disaster_type, location=self.district, description="Big Flood", date="2014-12-01",
                          status="Assessment")
        Disaster(**attributes).save()
        disasters = Disaster.objects(**attributes)

        self.assertEqual(1, disasters.count())

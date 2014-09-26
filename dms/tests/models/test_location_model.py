from dms.models.location import Location
from dms.tests.base import MongoTestCase


class TestLocationModel(MongoTestCase):

    def tearDown(self):
        Location.drop_collection()

    def test_should_save_location_with_no_parent(self):
        district = dict(name='Kampala', parent=None, type='district')

        Location(**district).save()
        saved_districts = Location.objects(**district)
        self.assertEqual(1, saved_districts.count())

    def test_should_save_location_with_a_parent(self):
        district = Location(**dict(name='Kampala', parent=None, type='district'))
        district.save()
        village = dict(name='Bukoto', parent=district, type='village')
        Location(**village).save()

        saved_villages = Location.objects(**village)
        self.assertEqual(1, saved_villages.count())

        saved_village = saved_villages[0]
        self.assertEqual(village['name'], saved_village.name)
        self.assertEqual(district['name'], saved_village.parent.name)




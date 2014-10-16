from dms.models.location import Location
from dms.tests.base import MongoTestCase


class TestLocationModel(MongoTestCase):

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

    def test_to_string_parent(self):
        district = dict(name='Kampala', parent=None, type='district')
        location = Location(**district).save()

        self.assertEqual('Kampala', str(location))

    def test_to_string_child(self):
        kampala = Location(**(dict(name='Kampala', parent=None, type='district'))).save()
        bukoto = Location(**(dict(name='Bukoto', parent=kampala, type='village'))).save()

        self.assertEqual('Kampala >> Bukoto', str(bukoto))

    def test_should_know_its_children(self):
        district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        bukoto = Location(**dict(name='Bukoto', parent=district, type='village')).save()
        wakiso = Location(**dict(name='Wakiso', parent=district, type='village')).save()

        district_children = district.children()

        self.assertEqual(2, len(district_children))
        self.assertIn(bukoto, district_children)
        self.assertIn(wakiso, district_children)

    def test_should_know_its_children_include_self(self):
        district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        bukoto = Location(**dict(name='Bukoto', parent=district, type='village')).save()
        wakiso = Location(**dict(name='Wakiso', parent=district, type='village')).save()

        district_children = district.children(include_self=True)

        self.assertEqual(3, len(district_children))
        self.assertIn(bukoto, district_children)
        self.assertIn(wakiso, district_children)
        self.assertIn(district, district_children)

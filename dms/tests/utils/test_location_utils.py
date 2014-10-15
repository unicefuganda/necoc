from dms.models import Location
from dms.tests.base import MongoTestCase
from dms.utils.location_utils import find_location_match
from django.test.utils import override_settings


class LocationUtilsTest(MongoTestCase):

    def setUp(self):
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()

    @override_settings(LOCATION_MATCH_LEVEL=0.8)
    def test_location_is_matched_given_match_level(self):
        self.assertEqual(self.village, find_location_match('bukota'))
        self.assertIsNone(find_location_match('bukotaaaaa'))
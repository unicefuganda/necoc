from dms.models import Location
from dms.tests.base import MongoTestCase
from dms.utils.location_utils import MessageLocationExtractor
from django.test.utils import override_settings


class LocationUtilsTest(MongoTestCase):

    def setUp(self):
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.bukoto = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()

    def test_no_location_is_mached_when_no_text_given(self):
        locator = MessageLocationExtractor(None)
        self.assertEqual(None, locator.best_match())

        locator = MessageLocationExtractor('')
        self.assertEqual(None, locator.best_match())

    @override_settings(MESSAGE_LOCATION_INDEX=3, MESSAGE_MILITARY_SEPARATOR='*')
    def test_district_identified_if_it_is_militarily_coded_and_matched(self):
        text = "NECOC * Fire * Kampala * There is fire over here baba"
        locator = MessageLocationExtractor(text)

        self.assertEqual(self.district, locator.best_match())

    @override_settings(LOCATION_MATCH_LEVEL=0.7, MESSAGE_LOCATION_INDEX=3, MESSAGE_MILITARY_SEPARATOR='*')
    def test_location_is_fuzzy_matched(self):
        text = "NECOC * Fire * Kampalaa * There is fire over here baba"
        locator = MessageLocationExtractor(text)

        self.assertEqual(self.district, locator.best_match())

        text = "NECOC * Fire * Kempela * There is fire over here baba"
        locator = MessageLocationExtractor(text)

        self.assertEqual(self.district, locator.best_match())

    @override_settings(LOCATION_MATCH_LEVEL=0.7, MESSAGE_LOCATION_INDEX=3, MESSAGE_MILITARY_SEPARATOR='*')
    def test_subcounty_is_identified_if_district_supplied(self):
        kampala_tc = Location(**dict(name='Kampala TC', parent=self.district, type='subcounty')).save()
        text = "NECOC * Fire * Kampala * Kampala TC * There is fire over here baba"
        locator = MessageLocationExtractor(text)

        self.assertEqual(kampala_tc, locator.best_match())

    @override_settings(LOCATION_MATCH_LEVEL=0.7, MESSAGE_LOCATION_INDEX=3, MESSAGE_MILITARY_SEPARATOR='*')
    def test_subcounty_is_fuzzy_matched_even_if_no_district_supplied(self):
        text = "NECOC * Fire * bukotoo * There is fire over here baba"
        locator = MessageLocationExtractor(text)

        self.assertEqual(self.bukoto, locator.best_match())

    @override_settings(MESSAGE_MILITARY_SEPARATOR=' ', MESSAGE_LOCATION_INDEX=3, LOCATION_MATCH_LEVEL=0.7)
    def test_blank_space_separator_still_fetches_subcounty(self):
        text = "NECOC Fire bukotoo There is fire over here baba"
        locator = MessageLocationExtractor(text)

        self.assertEqual(self.bukoto, locator.best_match())

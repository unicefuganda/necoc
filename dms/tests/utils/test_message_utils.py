import datetime
import pytz
from dms.models import Location, DisasterType, Disaster
from dms.tests.base import MongoTestCase
from django.test.utils import override_settings
from dms.utils.message_utils import MessageDisasterAssociator
from necoc import settings


class MessageUtilsTest(MongoTestCase):

    def setUp(self):
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.date_time = self.date_time.replace(tzinfo=pytz.utc)
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.fire_disaster_type = DisasterType(**dict(name='Flood', description="Some flood")).save()
        self.flood_disaster_type = DisasterType(**dict(name='Fire', description="Some raging fire")).save()
        self.storm_disaster_type = DisasterType(**dict(name='Storm', description="Heavy rain with thunderstorms")).save()
        self.fire_disaster = Disaster(**dict(name=self.fire_disaster_type, locations=[self.village], \
                                            status=settings.DISASTER_STATUSES[0], date=self.date_time)).save()
        self.flood_disaster = Disaster(**dict(name=self.flood_disaster_type, locations=[self.village], \
                                            status=settings.DISASTER_STATUSES[1], date=self.date_time)).save()
        self.storm_disaster = Disaster(**dict(name=self.storm_disaster_type, locations=[self.village], \
                                            status=settings.DISASTER_STATUSES[0], date=self.date_time)).save()

        self.text_format = "NECOC.%s. There is a fire"
        self.text = self.text_format % self.village.name

    def test_no_disaster_is_mached_when_no_text_given(self):
        associator = MessageDisasterAssociator(None)
        self.assertEqual(None, associator.match_disaster())

        associator = MessageDisasterAssociator('')
        self.assertEqual(None, associator.match_disaster())

    def test_associated_if_text_matched_accurately(self):
        associator = MessageDisasterAssociator(self.text)
        self.assertEqual("Fire", associator.match_disaster())

    def test_associated_if_text_matched_reasonably(self):
        associator = MessageDisasterAssociator('NECOC.KATAKWI floads have invaded')
        self.assertEqual("Flood", associator.match_disaster())

    def test_no_association_when_no_match_found(self):
        associator = MessageDisasterAssociator('NECOC.KATAKWI locusts have invaded')
        self.assertEqual(None, associator.match_disaster())

    @override_settings(DISASTER_ASSOCIATION_MATCH_RATIO=99)
    def test_no_association_when_accuracy_requirement_increased(self):
        associator = MessageDisasterAssociator('NECOC.KATAKWI floads have invaded')
        self.assertEqual(None, associator.match_disaster())

    @override_settings(DISASTER_ASSOCIATION_MATCH_RATIO=30)
    def test_associated_even_when_disaster_is_merely_implied(self):
        associator = MessageDisasterAssociator('NECOC.KATAKWI it has been raining heavily lately with cloudy skys all day')
        self.assertEqual("Flood", associator.match_disaster())

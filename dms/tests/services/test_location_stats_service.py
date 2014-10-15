import datetime
from dms.models import RapidProMessage, Location
from dms.services.location_stats import LocationStatsService
from dms.tests.base import MongoTestCase


class TestLocationStats(MongoTestCase):

    def setUp(self):
        self.location_name = 'Kampala'
        text = "NECOC %s fire baba fire" % self.location_name
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234, run_id=23243)
        self.district = Location(**dict(name=self.location_name, parent=None, type='district')).save()

    def test_should_retrieve_aggregated_messages_in_a_location(self):
        RapidProMessage(**self.message).save()
        message1 = self.message.copy()
        message1["phone_number"] = "12345"
        RapidProMessage(**message1).save()

        location_stats_service = LocationStatsService(self.location_name)
        message_stats = location_stats_service.aggregate_stats()

        self.assertEqual({'messages': 2}, message_stats)

    def test_should_return_0_if_location_not_existing(self):
        inexistant_location_name = "ayoyoooo location"

        location_stats_service = LocationStatsService(inexistant_location_name)
        message_stats = location_stats_service.aggregate_stats()

        self.assertEqual({'messages': 0}, message_stats)


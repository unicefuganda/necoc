import datetime
from dms.models import RapidProMessage, Location
from dms.services.location_stats import LocationStatsService, MultiLocationStatsService
from dms.tests.base import MongoTestCase


class LocationStatsTest(MongoTestCase):

    def setUp(self):
        self.location_name = 'Kampala'
        text = "NECOC %s fire baba fire" % self.location_name
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234, run_id=23243)
        self.district = Location(**dict(name=self.location_name, parent=None, type='district')).save()

    def test_should_retrieve_message_count_in_a_location(self):
        RapidProMessage(**self.message).save()
        message1 = self.message.copy()
        message1["phone_number"] = "12345"
        RapidProMessage(**message1).save()

        location_stats_service = LocationStatsService(self.district)
        stats = location_stats_service.aggregate_stats()
        message_stats = stats.messages

        self.assertEqual(2, message_stats.count)
        self.assertEqual(100, message_stats.percentage)

    def test_should_retrieve_messages_percentage_in_a_location(self):
        RapidProMessage(**self.message).save()
        message1 = self.message.copy()
        message1["text"] = "some message that is not coming from Kampala"
        RapidProMessage(**message1).save()

        location_stats_service = LocationStatsService(self.district)
        stats = location_stats_service.aggregate_stats()
        message_stats = stats.messages

        self.assertEqual(1, message_stats.count)
        self.assertEqual(50, message_stats.percentage)

    def test_should_return_0_if_location_not_existing(self):
        inexistant_location = None

        location_stats_service = LocationStatsService(inexistant_location)
        stats = location_stats_service.aggregate_stats()
        message_stats = stats.messages

        self.assertEqual(0, message_stats.count)
        self.assertEqual(0, message_stats.percentage)


class MultiLocationStatsTest(MongoTestCase):

    def setUp(self):
        self.location_name = 'Kampala'
        text = "NECOC %s fire baba fire" % self.location_name
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text=text, received_at=self.date_time, relayer_id=234, run_id=23243)
        self.kampala = Location(**dict(name=self.location_name, parent=None, type='district')).save()
        self.bukoto_name = 'Bukoto'
        self.bukoto = Location(**dict(name=self.bukoto_name, parent=None, type='district')).save()
        text = "NECOC %s flood" % self.bukoto_name
        self.message_bukoto = dict(phone_no=phone_number, text=text, received_at=self.date_time, relayer_id=234, run_id=23243)

    def test_should_retrieve_message_stats_in_all_locations(self):
        RapidProMessage(**self.message).save()
        RapidProMessage(**self.message_bukoto).save()

        multi_location_stats_service = MultiLocationStatsService()
        stats = multi_location_stats_service.stats()
        self.assertEqual(2, len(stats))

        self.assertEqual(1, stats['Kampala'].messages.count)
        self.assertEqual(50, stats['Kampala'].messages.percentage)

        self.assertEqual(1, stats['Bukoto'].messages.count)
        self.assertEqual(50, stats['Bukoto'].messages.percentage)

    def test_should_retrieve_message_stats_in_subcounties_when_district_name_supplied(self):
        RapidProMessage(**self.message).save()

        bugolobi_name = 'Bugolobi'
        Location(**dict(name=  bugolobi_name, parent=self.kampala, type='subcounty')).save()
        text = "NECOC %s flood" % bugolobi_name
        message_bugolobi = dict(phone_no='123444', text=text, received_at=self.date_time, relayer_id=234, run_id=23243)

        RapidProMessage(**message_bugolobi).save()

        multi_location_stats_service = MultiLocationStatsService(self.kampala.name)
        stats = multi_location_stats_service.stats()
        self.assertEqual(1, len(stats))

        self.assertEqual(1, stats['Bugolobi'].messages.count)
        self.assertEqual(50, stats['Bugolobi'].messages.percentage)

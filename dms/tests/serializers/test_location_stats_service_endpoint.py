import datetime
from dms.api.location_stats_service_endpoint import LocationStatsSerializer, StatsDetailsSerializer, \
    MultiLocationStatsSerializer
from dms.models import DisasterType, Disaster

from dms.models.location import Location
from dms.models.rapid_pro_message import RapidProMessage
from dms.services.location_stats import LocationStatsService, StatsDetails, LocationStats
from dms.tests.base import MongoTestCase


class LocationStatsServiceSerializersTest(MongoTestCase):
    def setUp(self):
        self.location_name = 'Kampala'
        text = "NECOC.%s. fire baba fire" % self.location_name
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234, run_id=23243)
        self.district = Location(**dict(name=self.location_name, parent=None, type='district')).save()

        RapidProMessage(**self.message).save()
        message1 = self.message.copy()
        message1["text"] = "some message that is not coming from Kampala"
        RapidProMessage(**message1).save()

    def test_should_serialize_stats_details(self):
        stats = StatsDetails(1, 50, 0.61)
        serialized_object = StatsDetailsSerializer(stats)
        serialized_data = {'count': 1, 'percentage': 50, 'reporter_ratio': 0.61}

        self.assertEqual(serialized_data, serialized_object.data)

    def test_should_serialize_disaster_and_message_stats(self):
        stats = StatsDetails(1, 50, 0.61)
        location_stats = LocationStats(stats, stats)

        serialized_object = LocationStatsSerializer(location_stats)
        serialized_data = {'messages': {'count': 1, 'percentage': 50, 'reporter_ratio': 0.61},
                           'disasters': {'count': 1, 'percentage': 50, 'reporter_ratio': 0.61}}

        self.assertEqual(serialized_data, serialized_object.data)

    def test_should_serialize_location_stats_service_integration(self):
        disaster_type = DisasterType(**dict(name='Flood', description="Some flood"))
        disaster_type.save()

        disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Flood", date="2014-12-01",
                             status="Assessment")

        Disaster(**disaster_attr).save()

        location_stats_service = LocationStatsService(location=self.district)
        queryset = location_stats_service.aggregate_stats()
        serialized_object = LocationStatsSerializer(queryset)
        serialized_data = {'messages': {'count': 1, 'percentage': 50, 'reporter_ratio': 0},
                           'disasters': {'count': 1, 'percentage': 100, 'reporter_ratio': 0}}

        self.assertEqual(serialized_data, serialized_object.data)


class MultiLocationStatsServiceSerializersTest(MongoTestCase):
    def setUp(self):
        self.location_name = 'Kampala'
        text = "NECOC.%s. fire baba fire" % self.location_name
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234, run_id=23243)
        self.district = Location(**dict(name=self.location_name, parent=None, type='district')).save()
        self.bukoto_name = 'Bukoto'
        self.bukoto = Location(**dict(name=self.bukoto_name, parent=None, type='district')).save()
        text = "NECOC.%s. flood" % self.bukoto_name
        self.message_bukoto = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234,
                                   run_id=23243)

        disaster_type = DisasterType(**dict(name='Flood', description="Some flood"))
        disaster_type.save()

        self.disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Flood",
                                  date="2014-12-01",
                                  status="Assessment")

    def test_should_retrieve_message_stats_in_all_locations(self):
        RapidProMessage(**self.message).save()
        RapidProMessage(**self.message_bukoto).save()
        Disaster(**self.disaster_attr).save()

        multi_location_serializer = MultiLocationStatsSerializer(location=None)
        serialized_object = multi_location_serializer

        expected_serialized_data = {'kampala': {'messages': {'count': 1, 'percentage': 50, 'reporter_ratio': 0},
                                                'disasters': {'count': 1, 'percentage': 100, 'reporter_ratio': 0}},
                                    'bukoto': {'messages': {'count': 1, 'percentage': 50, 'reporter_ratio': 0},
                                               'disasters': {'count': 0, 'percentage': 0, 'reporter_ratio': 0}}
                                   }

        self.assertEqual(expected_serialized_data, serialized_object.data)
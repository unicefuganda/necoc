import datetime

from dms.api.stats_summary_service_endpoint import SummaryStatsDetailsSerializer, SummaryStatsSerializer
from dms.models import DisasterType, Disaster
from dms.models.location import Location
from dms.models.rapid_pro_message import RapidProMessage
from dms.services.stats_summary import SummaryStatsDetails, SummaryStats, StatsSummaryService
from dms.tests.base import MongoTestCase


class StatsSummaryServiceSerializersTest(MongoTestCase):
    def setUp(self):
        self.location_name = 'Kampala'
        text = "NECOC %s fire baba fire" % self.location_name
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234, run_id=23243)
        self.district = Location(**dict(name=self.location_name, parent=None, type='district')).save()

        RapidProMessage(**self.message).save()
        message1 = self.message.copy()
        message1["text"] = "some message that is not coming from Kampala"
        RapidProMessage(**message1).save()

    def test_should_serialize_summary_stats_details(self):
        stats = SummaryStatsDetails(1, 2, {'Fire': 2, 'Flood': 4})
        serialized_object = SummaryStatsDetailsSerializer(stats)
        serialized_data = {'count': 1, 'affected': 2,
                           'types': {'Fire': 2, 'Flood': 4}}

        self.assertEqual(serialized_data, serialized_object.data)

    def test_should_serialize_summary_stats(self):
        disaster_stats = SummaryStatsDetails(1, 2, {'Fire': 2, 'Flood': 4})
        summary_stats = SummaryStats(disaster_stats)

        serialized_object = SummaryStatsSerializer(summary_stats)
        serialized_data = {'disasters': {'count': 1,
                                         'affected': 2, 'types': {'Fire': 2, 'Flood': 4}}}

        self.assertEqual(serialized_data, serialized_object.data)

    def test_should_serialize_summary_stats_service_integration(self):
        disaster_type = DisasterType(**dict(name='Flood', description="Some flood"))
        disaster_type.save()

        disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Flood", date="2014-12-01",
                             status="Assessment")

        Disaster(**disaster_attr).save()

        location_stats_service = StatsSummaryService(location=self.district)
        queryset = location_stats_service.aggregate_stats()
        serialized_object = SummaryStatsSerializer(queryset)
        serialized_data = {'disasters': {'count': 1,
                                         'affected': 1, 'types': {'Flood': 1}}}

        self.assertEqual(serialized_data, serialized_object.data)

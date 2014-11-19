from dms.models import Location, DisasterType, Disaster
from dms.services.stats_summary import StatsSummaryService
from dms.tests.base import MongoTestCase


class DisasterSummaryStatsTest(MongoTestCase):
    def setUp(self):
        self.disaster_type = DisasterType(**dict(name='Flood', description="Some flood")).save()

        self.kampala = Location(**dict(name='Kampala', type='district', parent=None)).save()
        self.bukoto = Location(**dict(name='Bukoto', type='subcounty', parent=self.kampala)).save()

        self.disaster_attr = dict(name=self.disaster_type, locations=[self.bukoto], description="Big Flood",
                                  date="2014-12-01", status="Assessment")

    def test_should_retrieve_message_count_affected_types_countrywide(self):
        wakiso = Location(**dict(name='Wakiso', type='district', parent=None)).save()
        wakiso_disaster_attr = self.disaster_attr.copy()
        wakiso_disaster_attr['locations'] = [wakiso]
        Disaster(**wakiso_disaster_attr).save()

        Disaster(**self.disaster_attr).save()

        attr2 = self.disaster_attr.copy()
        attr2["status"] = "Closed"
        Disaster(**attr2).save()

        location_stats_service = StatsSummaryService(location=None)
        stats = location_stats_service.aggregate_stats()
        disasters_stats = stats.disasters

        self.assertEqual(3, disasters_stats.count)
        self.assertEqual(2, disasters_stats.affected)
        self.assertEqual({'Flood': 3}, disasters_stats.types)

    def test_should_retrieve_message_count_affected_types_of_a_district(self):
        Disaster(**self.disaster_attr).save()
        attr2 = self.disaster_attr.copy()
        attr2["status"] = "Closed"
        Disaster(**attr2).save()

        location_stats_service = StatsSummaryService(location=self.kampala)
        stats = location_stats_service.aggregate_stats()
        disasters_stats = stats.disasters

        self.assertEqual(2, disasters_stats.count)
        self.assertEqual(1, disasters_stats.affected)
        self.assertEqual({'Flood': 2}, disasters_stats.types)

    def test_should_retrieve_message_count_affected_types_of_a_subcounty(self):
        Disaster(**self.disaster_attr).save()
        fire_type = DisasterType(**dict(name='Fire', description="whatever")).save()
        attr2 = self.disaster_attr.copy()
        attr2["locations"] = [Location(**dict(name='Location that is not Kampala', type='district')).save()]
        attr2["name"] = fire_type
        Disaster(**attr2).save()

        location_stats_service = StatsSummaryService(location=self.bukoto)
        stats = location_stats_service.aggregate_stats()
        disasters_stats = stats.disasters

        self.assertEqual(1, disasters_stats.count)

        self.assertEqual(1, disasters_stats.affected)
        self.assertEqual({'Flood': 1}, disasters_stats.types)

    def test_types_of_a_subcounty(self):
        Disaster(**self.disaster_attr).save()
        fire_type = DisasterType(**dict(name='Fire', description="whatever")).save()
        attr2 = self.disaster_attr.copy()
        attr2["name"] = fire_type
        Disaster(**attr2).save()

        location_stats_service = StatsSummaryService(location=self.bukoto)
        stats = location_stats_service.aggregate_stats()
        disasters_stats = stats.disasters

        self.assertEqual(2, disasters_stats.count)

        self.assertEqual(1, disasters_stats.affected)
        self.assertEqual({'Flood': 1, 'Fire': 1}, disasters_stats.types)

    def test_should_return_0_if_no_disaster_everywhere(self):
        location_stats_service = StatsSummaryService(location=self.bukoto)
        stats = location_stats_service.aggregate_stats()
        disasters_stats = stats.disasters

        self.assertEqual(0, disasters_stats.count)

        self.assertEqual(0, disasters_stats.affected)
        self.assertEqual({}, disasters_stats.types)


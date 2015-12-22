import datetime
from django.test.utils import override_settings

from dms.models import Location, DisasterType, Disaster
from dms.tests.base import MongoAPITestCase

@override_settings(REST_FRAMEWORK={})
class StatsSummaryServiceEndpointTest(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/stats-summary/'

    def setUp(self):
        self.location_name = 'Kampala'
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.kampala = Location(**dict(name=self.location_name, parent=None, type='district')).save()
        self.bukoto_name = 'Bukoto'
        self.bukoto = Location(**dict(name=self.bukoto_name, parent=None, type='district')).save()
        self.disaster_type = DisasterType(**dict(name='Flood', description="Some flood")).save()
        self.disaster_attr = dict(name=self.disaster_type, locations=[self.kampala], description="Big Flood",
                                  date=self.date_time,
                                  status="Assessment")

        self.disaster_attr_bukoto = self.disaster_attr.copy()
        self.disaster_attr_bukoto["locations"] = [self.bukoto]

    def test_should_retrieve_summary_stats_in_the_country(self):
        Disaster(**self.disaster_attr).save()
        Disaster(**self.disaster_attr_bukoto).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        response = self.client.get(self.API_ENDPOINT, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_should_retrieve_message_stats_in_district(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()
        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        url = '%s?location=%s' % (self.API_ENDPOINT, str(self.kampala.name.lower()))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

    def test_should_retrieve_message_stats_in_subcounty(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()
        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 1,
                                                  'affected': 1, 'types': {'Flood': 1}}}

        url = '%s?location=%s' % (self.API_ENDPOINT, 'bugolobi')
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

    def test_should_filter_summary_stats_in_country_by_date(self):
        Disaster(**self.disaster_attr).save()
        Disaster(**self.disaster_attr_bukoto).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s&to=%s' % (from_, to_))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s' % to_)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        response = self.client.get(self.API_ENDPOINT + '?format=json&to=%s' % from_)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_district_by_date(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '?location=%sformat=json&from=%s&to=%s' % (str(self.kampala.name.lower()), from_, to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        url = self.API_ENDPOINT + '?location=%sformat=json&from=%s' % (str(self.kampala.name.lower()), to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%sformat=json&to=%s' % (str(self.kampala.name.lower()), from_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_subcounty_by_date(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 1,
                                                  'affected': 1, 'types': {'Flood': 1}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&to=%s' % ('Bugolobi', from_, to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s' % ('Bugolobi', to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%s&format=json&to=%s' % ('Bugolobi', from_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

    def test_should_filter_stats_in_country_by_disaster_types(self):
        kampala_disaster = Disaster(**self.disaster_attr).save()
        bukoto_disaster = Disaster(**self.disaster_attr_bukoto).save()


        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        response = self.client.get(self.API_ENDPOINT + '?format=json&disaster_type=%s' % str(self.disaster_type.id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        disaster_type2 = DisasterType(**dict(name='Fire', description="Some fire")).save()
        disaster_attr = self.disaster_attr.copy()
        disaster_attr['name'] = disaster_type2
        Disaster(**disaster_attr).save()

        expected_serialized_data = {'disasters': {'count': 1,
                                                  'affected': 1, 'types': {'Fire': 1}}}

        response = self.client.get(self.API_ENDPOINT + '?format=json&disaster_type=%s' % str(disaster_type2.id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_district_by_disaster_type(self):

        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        disaster_bugolobi = Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        url = self.API_ENDPOINT + '?location=%s&format=json&disaster_type=%s' % (str(self.kampala.name.lower()), str(self.disaster_type.id))
        response = self.client.get(url, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_subcounty_by_disaster_type(self):

        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        disaster_bugolobi = Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 1,
                                                  'affected': 1, 'types': {'Flood': 1}}}

        url = self.API_ENDPOINT + '?location=%s&format=json&disaster_type=%s' % ('Bugolobi', str(self.disaster_type.id))
        response = self.client.get(url, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_should_filter_stats_in_country_by_date_and_disaster_type(self):
        kampala_disaster = Disaster(**self.disaster_attr).save()
        bukoto_disaster = Disaster(**self.disaster_attr_bukoto).save()


        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s&to=%s&disaster_type=%s'% (from_,
                                                                                                       to_, str(self.disaster_type.id)))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        other_type = DisasterType(**dict(name='Fire', description="Some flood")).save()

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}


        url = self.API_ENDPOINT + '?format=json&from=%s&to=%s&disaster_type=%s' % (from_, to_, str(other_type.id))
        response = self.client.get(url, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?format=json&from=%s&disaster_type=%s' % (to_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?format=json&to=%s&disaster_type=%s' % (from_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_district_by_date_and_disater_type(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        disaster_bugolobi = Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&to=%s&disaster_type=%s' % (str(self.kampala.name.lower()),
                                                                                      from_, to_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        other_type = DisasterType(**dict(name='Fire', description="Some flood")).save()

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&to=%s&disaster_type=%s' % (str(self.kampala.name.lower()), from_, to_, str(other_type.id))
        response = self.client.get(url, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&disaster_type=%s' % (str(self.kampala.name.lower()),
                                                                                      to_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%s&format=json&to=%s&disaster_type=%s' % (str(self.kampala.name.lower()),
                                                                                      from_, str(self.disaster_type.id))

        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_subcounty_by_date_and_disater_type(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        disaster_bugolobi = Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 1,
                                                  'affected': 1, 'types': {'Flood': 1}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&to=%s&disaster_type=%s' % ('Bugolobi',
                                                                                      from_, to_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        other_type = DisasterType(**dict(name='Fire', description="Some flood")).save()

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&to=%s&disaster_type=%s' % ('Bugolobi', from_, to_, str(other_type.id))
        response = self.client.get(url, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&disaster_type=%s' % ('Bugolobi',
                                                                                      to_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%s&format=json&to=%s&disaster_type=%s' % ('Bugolobi',
                                                                                      from_, str(self.disaster_type.id))

        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_in_country_empty_GET_parameter_query(self):
        Disaster(**self.disaster_attr).save()
        Disaster(**self.disaster_attr_bukoto).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s&to=%s&disaster_type=' % (from_, to_))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s&disaster_type=&to=' % to_)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        response = self.client.get(self.API_ENDPOINT + '?format=json&to=%s&disaster_type=&from=' % from_)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_district_empty_GET_parameter_query(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 2,
                                                  'affected': 2, 'types': {'Flood': 2}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&to=%s&disaster_type=' % (str(self.kampala.name.lower()), from_, to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&disaster_type=&to=' % (str(self.kampala.name.lower()), to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%s&format=json&to=%s' % (str(self.kampala.name.lower()), from_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

    def test_subcounty_empty_GET_parameter_query(self):
        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'disasters': {'count': 1,
                                                  'affected': 1, 'types': {'Flood': 1}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&to=%s&disaster_type=' % ('Bugolobi', from_, to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'disasters': {'count': 0,
                                                  'affected': 0, 'types': {}}}

        url = self.API_ENDPOINT + '?location=%s&format=json&from=%s&disaster_type=&to=' % ('Bugolobi', to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '?location=%s&format=json&to=%s' % ('Bugolobi', from_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)
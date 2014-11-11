import datetime

from dms.models import Location, DisasterType, Disaster
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoAPITestCase


class LocationStatsServiceEndpointTest(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/location-stats/'

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
        self.message_bukoto = dict(phone_no=phone_number, text=text, received_at=self.date_time, relayer_id=234,
                                   run_id=23243)

        self.disaster_type = DisasterType(**dict(name='Flood', description="Some flood")).save()
        self.disaster_attr = dict(name=self.disaster_type, locations=[self.kampala], description="Big Flood",
                                  date=self.date_time,
                                  status="Assessment")

        self.disaster_attr_bukoto = self.disaster_attr.copy()
        self.disaster_attr_bukoto["locations"] = [self.bukoto]

    def test_should_retrieve_message_stats_in_all_locations(self):
        RapidProMessage(**self.message).save()
        RapidProMessage(**self.message_bukoto).save()
        Disaster(**self.disaster_attr).save()
        Disaster(**self.disaster_attr_bukoto).save()

        expected_serialized_data = {'kampala': {'messages': {'count': 1, 'percentage': 50},
                                                'disasters': {'count': 1, 'percentage': 50}},
                                    'bukoto': {'messages': {'count': 1, 'percentage': 50},
                                               'disasters': {'count': 1, 'percentage': 50}}
        }

        response = self.client.get(self.API_ENDPOINT, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_should_retrieve_message_stats_in_subcounties_in_district(self):
        RapidProMessage(**self.message).save()

        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()
        text = "NECOC %s flood" % bugolobi_name
        message_bugolobi = dict(phone_no='123444', text=text, received_at=self.date_time, relayer_id=234, run_id=23243)

        RapidProMessage(**message_bugolobi).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'bugolobi': {'messages': {'count': 1, 'percentage': 50},
                                                 'disasters': {'count': 1, 'percentage': 50}}}

        url = '%s%s/' % (self.API_ENDPOINT, str(self.kampala.name.lower()))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

    def test_should_filter_stats_in_all_locations_by_date(self):
        RapidProMessage(**self.message).save()
        RapidProMessage(**self.message_bukoto).save()
        Disaster(**self.disaster_attr).save()
        Disaster(**self.disaster_attr_bukoto).save()

        expected_serialized_data = {'kampala': {'messages': {'count': 1, 'percentage': 50},
                                                'disasters': {'count': 1, 'percentage': 50}},
                                    'bukoto': {'messages': {'count': 1, 'percentage': 50},
                                               'disasters': {'count': 1, 'percentage': 50}}
        }

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s&to=%s' % (from_, to_))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'kampala': {'messages': {'count': 0, 'percentage': 0},
                                                'disasters': {'count': 0, 'percentage': 0}},
                                    'bukoto': {'messages': {'count': 0, 'percentage': 0},
                                               'disasters': {'count': 0, 'percentage': 0}}
                                    }


        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s' % to_)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        response = self.client.get(self.API_ENDPOINT + '?format=json&to=%s' % from_)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_subcounties_in_district_by_date(self):
        RapidProMessage(**self.message).save()

        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()
        text = "NECOC %s flood" % bugolobi_name
        message_bugolobi = dict(phone_no='123444', text=text, received_at=self.date_time, relayer_id=234, run_id=23243)

        RapidProMessage(**message_bugolobi).save()

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        Disaster(**disaster_attr_bugolobi).save()

        expected_serialized_data = {'bugolobi': {'messages': {'count': 1, 'percentage': 50},
                                                 'disasters': {'count': 1, 'percentage': 50}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '%s/?format=json&from=%s&to=%s' % (str(self.kampala.name.lower()), from_, to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)


        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'bugolobi': {'messages': {'count': 0, 'percentage': 0},
                                                'disasters': {'count': 0, 'percentage': 0}}}

        url = self.API_ENDPOINT + '%s/?format=json&from=%s' % (str(self.kampala.name.lower()), to_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '%s/?format=json&to=%s' % (str(self.kampala.name.lower()), from_)
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

        self.assertEqual(expected_serialized_data, response.data)

    def test_should_filter_stats_in_all_locations_by_disaster_types(self):
        kampala_disaster = Disaster(**self.disaster_attr).save()
        bukoto_disaster = Disaster(**self.disaster_attr_bukoto).save()

        message_attr = self.message.copy()
        message_attr['disaster'] = kampala_disaster
        RapidProMessage(**message_attr).save()
        RapidProMessage(**self.message_bukoto).save()

        expected_serialized_data = {'kampala': {'messages': {'count': 1, 'percentage': 100},
                                                'disasters': {'count': 1, 'percentage': 50}},
                                    'bukoto': {'messages': {'count': 0, 'percentage': 0},
                                               'disasters': {'count': 1, 'percentage': 50}}
        }

        response = self.client.get(self.API_ENDPOINT + '?format=json&disaster_type=%s' % str(self.disaster_type.id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        disaster_type2 = DisasterType(**dict(name='Fire', description="Some fire")).save()
        disaster_attr = self.disaster_attr.copy()
        disaster_attr['name'] = disaster_type2
        Disaster(**disaster_attr).save()


        expected_serialized_data = {'kampala': {'messages': {'count': 0, 'percentage': 0},
                                                'disasters': {'count': 1, 'percentage': 100}},
                                    'bukoto': {'messages': {'count': 0, 'percentage': 0},
                                               'disasters': {'count': 0, 'percentage': 0}}
                                    }

        response = self.client.get(self.API_ENDPOINT + '?format=json&disaster_type=%s' % str(disaster_type2.id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_filter_stats_in_subcounties_in_district_by_disaster_type(self):
        RapidProMessage(**self.message).save()

        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()
        text = "NECOC %s flood" % bugolobi_name
        message_bugolobi = dict(phone_no='123444', text=text, received_at=self.date_time, relayer_id=234, run_id=23243)

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        disaster_bugolobi = Disaster(**disaster_attr_bugolobi).save()
        message_bugolobi['disaster'] = disaster_bugolobi

        RapidProMessage(**message_bugolobi).save()

        expected_serialized_data = {'bugolobi': {'messages': {'count': 1, 'percentage': 100},
                                                 'disasters': {'count': 1, 'percentage': 50}}}

        url = self.API_ENDPOINT + '%s/?format=json&disaster_type=%s' % (str(self.kampala.name.lower()), str(self.disaster_type.id))
        response = self.client.get(url, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

    def test_should_filter_stats_in_all_locations_by_date_and_disaster_type(self):
        kampala_disaster = Disaster(**self.disaster_attr).save()
        bukoto_disaster = Disaster(**self.disaster_attr_bukoto).save()

        message_attr = self.message.copy()
        message_attr['disaster'] = kampala_disaster
        RapidProMessage(**message_attr).save()
        RapidProMessage(**self.message_bukoto).save()

        expected_serialized_data = {'kampala': {'messages': {'count': 1, 'percentage': 100},
                                                'disasters': {'count': 1, 'percentage': 50}},
                                    'bukoto': {'messages': {'count': 0, 'percentage': 0},
                                               'disasters': {'count': 1, 'percentage': 50}}
        }

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        response = self.client.get(self.API_ENDPOINT + '?format=json&from=%s&to=%s&disaster_type=%s'% (from_,
                                                                                                       to_, str(self.disaster_type.id)))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'kampala': {'messages': {'count': 0, 'percentage': 0},
                                                'disasters': {'count': 0, 'percentage': 0}},
                                    'bukoto': {'messages': {'count': 0, 'percentage': 0},
                                               'disasters': {'count': 0, 'percentage': 0}}
                                    }

        other_type = DisasterType(**dict(name='Fire', description="Some flood")).save()

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

    def test_filter_stats_in_subcounties_in_district_by_date_and_disater_type(self):
        RapidProMessage(**self.message).save()

        bugolobi_name = 'Bugolobi'
        bugolobi = Location(**dict(name=bugolobi_name, parent=self.kampala, type='subcounty')).save()
        text = "NECOC %s flood" % bugolobi_name
        message_bugolobi = dict(phone_no='123444', text=text, received_at=self.date_time, relayer_id=234, run_id=23243)

        Disaster(**self.disaster_attr).save()
        disaster_attr_bugolobi = self.disaster_attr.copy()
        disaster_attr_bugolobi["locations"] = [bugolobi]
        disaster_bugolobi = Disaster(**disaster_attr_bugolobi).save()
        message_bugolobi['disaster'] = disaster_bugolobi

        RapidProMessage(**message_bugolobi).save()

        expected_serialized_data = {'bugolobi': {'messages': {'count': 1, 'percentage': 100},
                                                 'disasters': {'count': 1, 'percentage': 50}}}

        from_ = self.date_time - datetime.timedelta(days=1)
        from_ = str(from_.date())
        to_ = self.date_time + datetime.timedelta(days=1)
        to_ = str(to_.date())

        url = self.API_ENDPOINT + '%s/?format=json&from=%s&to=%s&disaster_type=%s' % (str(self.kampala.name.lower()),
                                                                                      from_, to_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        expected_serialized_data = {'bugolobi': {'messages': {'count': 0, 'percentage': 0},
                                                'disasters': {'count': 0, 'percentage': 0}}}

        other_type = DisasterType(**dict(name='Fire', description="Some flood")).save()

        url = self.API_ENDPOINT + '%s/?format=json&from=%s&to=%s&disaster_type=%s' % (str(self.kampala.name.lower()), from_, to_, str(other_type.id))
        response = self.client.get(url, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '%s/?format=json&from=%s&disaster_type=%s' % (str(self.kampala.name.lower()),
                                                                                      to_, str(self.disaster_type.id))
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

        url = self.API_ENDPOINT + '%s/?format=json&to=%s&disaster_type=%s' % (str(self.kampala.name.lower()),
                                                                                      from_, str(self.disaster_type.id))

        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_serialized_data, response.data)

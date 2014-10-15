import datetime

from dms.models import Location
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoAPITestCase


class LocationStatsServiceEndpointTest(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/location-stats/'

    def setUp(self):
        self.location_name = 'Kampala'
        text = "NECOC %s fire baba fire" % self.location_name
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"
        self.message = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234, run_id=23243)
        self.district = Location(**dict(name=self.location_name, parent=None, type='district')).save()
        self.bukoto_name = 'Bukoto'
        self.bukoto = Location(**dict(name=self.bukoto_name, parent=None, type='district')).save()
        text = "NECOC %s flood" % self.bukoto_name
        self.message_bukoto = dict(phone_no=phone_number, text=text, received_at=date_time, relayer_id=234, run_id=23243)

    def test_should_retrieve_message_stats_in_all_locations(self):
        RapidProMessage(**self.message).save()
        RapidProMessage(**self.message_bukoto).save()

        expected_serialized_data = {'kampala': {'messages': {'count': 1, 'percentage': 50}},
                                    'bukoto': {'messages': {'count': 1, 'percentage': 50}}
                                    }

        response = self.client.get(self.API_ENDPOINT, format='json')
        self.assertEqual(200, response.status_code)


        self.assertEqual(expected_serialized_data, response.data)

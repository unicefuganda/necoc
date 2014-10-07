import datetime
from dms.models import Location, MobileUser, Disaster, DisasterType
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoAPITestCase


class RapidProEndPointTest(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/rapid-pro/'

    def setUp(self):
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.expected_message = dict(phone="+256775019449", text="There is a fire", time=self.date_time, relayer=234,
                                     run=23243)
        self.message = dict(phone_no="+256775019449", text="There is a fire", received_at=self.date_time,
                            relayer_id=234, run_id=23243)
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = MobileUser(**dict(name='timothy', phone="+256775019449",
                                             location=self.village, email=None)).save()

        disaster_type = DisasterType(**dict(name="Fire", description="Fire")).save()
        disaster_attributes = dict(name=disaster_type, location=self.district,
                                   description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")
        self.disaster = Disaster(**disaster_attributes).save()

    def _api_url(self, id):
        return "%s%s/" % (self.API_ENDPOINT, str(id))

    def test_should_create_rapid_pro_message(self):
        response = self.client.post(self.API_ENDPOINT, data=self.expected_message)
        self.assertEqual(201, response.status_code)

        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())

    def test_should_get_rapid_pro_message(self):
        RapidProMessage(**self.message).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.expected_message, response.data[0])
        self.assertEqual('NECOC Volunteer', response.data[0]['source'])
        self.assertEqual('Kampala >> Bukoto', response.data[0]['location'])
        self.assertIsNotNone(response.data[0]['id'])

    def test_should_filter_messages_by_location(self):
        RapidProMessage(**self.message).save()
        wakiso = Location(**(dict(name='Wakiso', type='village'))).save()

        response = self.client.get(self.API_ENDPOINT, {"location": wakiso.id, "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

        other_phone_number = '1234'
        other_message_options = dict(phone_no=other_phone_number, text="There is a fire", received_at=self.date_time,
                                     relayer_id=234, run_id=23243)
        MobileUser(**dict(name='timothy', phone=other_phone_number, location=wakiso)).save()
        RapidProMessage(**other_message_options).save()

        response = self.client.get(self.API_ENDPOINT, {"location": wakiso.id, "format": "json"})

        expected_message = {'phone': other_phone_number, 'time': self.date_time, 'relayer': 234, 'run': 23243,
                            'text': u'There is a fire'}

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(expected_message, response.data[0])
        self.assertEqual('NECOC Volunteer', response.data[0]['source'])
        self.assertEqual(wakiso.name, response.data[0]['location'])

    def test_location_filter_should_return_messages_in_all_children_location(self):
        bukoto_message = RapidProMessage(**self.message).save()
        wakiso = Location(**(dict(name='Wakiso', type='village', parent=self.district))).save()
        other_phone_number = '1234'
        other_message_options = dict(phone_no=other_phone_number, text="There is a fire", received_at=self.date_time,
                                     relayer_id=234, run_id=23243)
        MobileUser(**dict(name='timothy', phone=other_phone_number, location=wakiso)).save()
        wakiso_message = RapidProMessage(**other_message_options).save()

        response = self.client.get(self.API_ENDPOINT, {"location": self.district.id, "format": "json"})

        wakiso_expected_message = {'phone': other_phone_number, 'time': self.date_time, 'relayer': 234, 'run': 23243,
                                   'text': u'There is a fire', 'disaster': None}
        wakiso_expected_message = dict(wakiso_expected_message.items() + {
            'source': 'NECOC Volunteer', 'id': str(wakiso_message.id), 'location': str(wakiso)}.items())

        bukoto_expected_message = dict(self.expected_message.items() + {
            'source': 'NECOC Volunteer', 'id': str(bukoto_message.id), 'disaster': None,
            'location': str(self.village)}.items())

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertIn(wakiso_expected_message, response.data)
        self.assertIn(bukoto_expected_message, response.data)

    def test_should_update_disaster_field_with_put(self):
        message = RapidProMessage(**self.message).save()

        data = self.expected_message.copy()
        data['disaster'] = self.disaster.id

        response = self.client.put(self._api_url(message.id), data=data)
        self.assertEqual(200, response.status_code)

        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())
        self.assertEqual(self.disaster, retrieved_message[0].disaster)

    def test_should_update_disaster_field_using_a_patch(self):
        message = RapidProMessage(**self.message).save()

        response = self.client.patch(self._api_url(message.id), data=dict(disaster=self.disaster.id))
        self.assertEqual(200, response.status_code)

        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())
        self.assertEqual(self.disaster, retrieved_message[0].disaster)

    def test_should_update_disaster_field_with_post_is_also_supported_for_phantomjs_sake(self):
        message = RapidProMessage(**self.message).save()

        response = self.client.post(self._api_url(message.id), data=dict(disaster=self.disaster.id))
        self.assertEqual(200, response.status_code)

        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())
        self.assertEqual(self.disaster, retrieved_message[0].disaster)

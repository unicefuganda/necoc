import datetime
import pytz
from dms.api.rapid_pro_endpoint import RAPID_PRO_TIME_FORMAT
from dms.models import Location, UserProfile, Disaster, DisasterType
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoAPITestCase


class RapidProEndPointTest(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/rapid-pro/'

    def setUp(self):
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.date_time = self.date_time.replace(tzinfo=pytz.utc)
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = UserProfile(**dict(name='timothy', phone="+256775019449",
                                             location=self.village, email=None)).save()

        self.fire_type = DisasterType(**dict(name="Fire", description="Fire")).save()
        disaster_attributes = dict(name=self.fire_type, locations=[self.district],
                                   description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")
        self.disaster = Disaster(**disaster_attributes).save()

        self.text_format = "NECOC %s There is a fire"
        text = self.text_format % self.village.name
        self.expected_message = dict(phone="+256775019449", text=text, time=self.date_time, relayer=234,
                                     run=23243)
        self.message = dict(phone_no="+256775019449", text=text, received_at=self.date_time,
                            relayer_id=234, run_id=23243)

    def _api_url(self, id):
        return "%s%s/" % (self.API_ENDPOINT, str(id))

    def test_should_create_rapid_pro_message(self):
        self.expected_message['time'] = self.date_time.strftime(RAPID_PRO_TIME_FORMAT)
        response = self.client.post(self.API_ENDPOINT, data=self.expected_message)
        self.assertEqual(201, response.status_code)

        del self.message['received_at']
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
        other_message_options = dict(phone_no=other_phone_number, text=self.text_format % wakiso.name, received_at=self.date_time,
                                     relayer_id=234, run_id=23243)
        RapidProMessage(**other_message_options).save()

        response = self.client.get(self.API_ENDPOINT, {"location": wakiso.id, "format": "json"})

        expected_message = {'phone': other_phone_number, 'time': self.date_time, 'relayer': 234, 'run': 23243,
                            'text': self.text_format % wakiso.name}

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(expected_message, response.data[0])
        self.assertEqual('NECOC Volunteer', response.data[0]['source'])
        self.assertEqual(wakiso.name, response.data[0]['location'])

    def test_location_filter_should_return_messages_in_all_children_location(self):
        bukoto_message = RapidProMessage(**self.message).save()
        wakiso = Location(**(dict(name='Wakiso', type='village', parent=self.district))).save()
        other_phone_number = '1234'
        other_message_options = dict(phone_no=other_phone_number, text=self.text_format % wakiso.name, received_at=self.date_time,
                                     relayer_id=234, run_id=23243)
        UserProfile(**dict(name='timothy', phone=other_phone_number, location=wakiso)).save()
        wakiso_message = RapidProMessage(**other_message_options).save()

        response = self.client.get(self.API_ENDPOINT, {"location": self.district.id, "format": "json"})

        wakiso_expected_message = {'phone': other_phone_number, 'time': self.date_time, 'relayer': 234, 'run': 23243,
                                   'text': self.text_format % wakiso.name, 'disaster': None}
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

        self.expected_message['time'] = self.date_time.replace(tzinfo=None)
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

    def test_should_filter_messages_by_disaster_association(self):
        uncategorized_message = RapidProMessage(**self.message).save()
        message_2 = self.message.copy()
        message_2['text'] = 'some other text'
        message_2['disaster'] = self.disaster

        categorized_message = RapidProMessage(**message_2).save()

        response = self.client.get(self.API_ENDPOINT, {"disaster": "", "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(str(uncategorized_message.id), response.data[0]['id'])
        self.assertDictContainsSubset(self.expected_message, response.data[0])

        response = self.client.get(self.API_ENDPOINT, {"disaster": str(self.disaster.id), "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(str(categorized_message.id), response.data[0]['id'])
        expected_message2= self.expected_message.copy()
        expected_message2['text'] = message_2['text']
        self.assertDictContainsSubset(expected_message2, response.data[0])

    def test_should_filter_messages_by_disaster_type(self):
        message_attr = self.message.copy()
        message_attr['disaster'] = self.disaster
        fire_message = RapidProMessage(**message_attr).save()
        flood_type = DisasterType(**dict(name="Flood", description="Flood")).save()

        response = self.client.get(self.API_ENDPOINT, {"disaster_type": str(self.fire_type.id), "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(str(fire_message.id), response.data[0]['id'])
        self.assertDictContainsSubset(self.expected_message, response.data[0])

        response = self.client.get(self.API_ENDPOINT, {"disaster_type": str(flood_type.id), "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_should_filter_messages_by_date_range(self):
        message_attr = self.message.copy()
        date_1_jan = datetime.datetime(2014, 01, 01)
        message_attr['received_at'] = date_1_jan
        message_now = RapidProMessage(**message_attr).save()

        message_attr2 = self.message.copy()
        date_3_jan = datetime.datetime(2014, 01, 03)
        message_attr2['received_at'] = date_3_jan
        message_2days_later = RapidProMessage(**message_attr2).save()

        response = self.client.get(self.API_ENDPOINT, {"to": "2014-01-02", "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(str(message_now.id), response.data[0]['id'])
        expected_message = self.expected_message.copy()
        expected_message['time'] = date_1_jan.replace(tzinfo=pytz.utc)
        self.assertDictContainsSubset(expected_message, response.data[0])

        response = self.client.get(self.API_ENDPOINT, {"from": "2014-01-02", "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(str(message_2days_later.id), response.data[0]['id'])
        expected_message2 = self.expected_message.copy()
        expected_message2['time'] = date_3_jan.replace(tzinfo=pytz.utc)
        self.assertDictContainsSubset(expected_message2, response.data[0])

        response = self.client.get(self.API_ENDPOINT, {"from": "2014-01-02", "to": "2014-01-02",  "format": "json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

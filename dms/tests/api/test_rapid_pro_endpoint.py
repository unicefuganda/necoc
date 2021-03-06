import datetime
import collections
from django.test.utils import override_settings
from mongoengine.django.auth import Group, Permission, ContentType
import pytz
import urllib2
import json
from rest_framework_csv.renderers import CSVRenderer
from dms.api.rapid_pro_endpoint import RAPID_PRO_TIME_FORMAT
from dms.models import Location, UserProfile, Disaster, DisasterType, SentMessage, User, AdminSetting
from dms.models.rapid_pro_message import RapidProMessage
from dms.tests.base import MongoAPITestCase
from django.conf import settings
from dms.utils.rapidpro_message_utils import split_text


def dict_replace(param, replace, datadict):
    for key, value in datadict.items():
        if key == param:
            datadict[key] = replace
    return datadict


class RapidProEndPointTest(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/rapid-pro/'
    CSV_ENDPOINT = '/api/v1/csv-messages/'

    def setUp(self):
        self.date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        self.date_time = self.date_time.replace(tzinfo=pytz.utc)
        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = UserProfile(**dict(name='timothy', phone="+256775019449",
                                             location=self.village, email=None)).save()

        self.fire_type = DisasterType(**dict(name="Fire", description="Fire")).save()
        disaster_attributes = dict(name=self.fire_type, locations=[self.district],
                                   description="Big Fire", date="2014-12-01 00:00:00", status="Assessment")
        self.disaster = Disaster(**disaster_attributes).save()

        self.text_format = "NECOC.%s. There is a fire"
        text = self.text_format % self.village.name
        self.expected_message = dict(phone="+256775019449", text=text, time=self.date_time, relayer=234,
                                     run=23243)
        self.message = dict(phone_no="+256775019449", text=text, received_at=self.date_time,
                            relayer_id=234, run_id=23243)

        self.api_user, created = User.objects.get_or_create(**dict(username='admin'))
        self.auto_message_response = dict(phone_numbers=[u'+256775019449'], text=settings.AUTO_RESPONSE_MESSAGE)

        self.cao_group, created = Group.objects.get_or_create(name='CAO')
        self.cao_user = User.objects.create(username='klaCAO', group=self.cao_group, email='kla@cao.ug')
        self.cao_user.set_password('password')
        self.login_url = '/login/'
        self.login_data = {
            'username': 'klaCAO',
            'password': 'password'
        }

        AdminSetting(**dict(name='enable_automatic_response')).save()
        AdminSetting(**dict(name='enable_volunteer_profiles')).save()

    def _api_url(self, id):
        return "%s%s/" % (self.API_ENDPOINT, str(id))

    def test_should_create_rapid_pro_message(self):
        self.expected_message['time'] = self.date_time.strftime(RAPID_PRO_TIME_FORMAT)
        response = self.client.post(self.API_ENDPOINT, data=self.expected_message)
        self.assertEqual(201, response.status_code)

        del self.message['received_at']
        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())

    def test_should_create_rapid_pro_message_from_wacky_format(self):
        normal_time = self.date_time.strftime(RAPID_PRO_TIME_FORMAT)
        rapid_pro_time = normal_time + ".234567Z"
        self.expected_message['time'] = rapid_pro_time
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
        self.assertEqual(self.mobile_user.name, response.data[0]['source'])
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

    def test_location_filter_should_return_messages_in_all_children_location_and_in_order(self):
        Disaster.objects.delete() #Remove all disasters to avoid interference with this test
        bukoto_message = RapidProMessage(**self.message).save()
        wakiso = Location(**(dict(name='Wakiso', type='village', parent=self.district))).save()
        other_phone_number = '1234'
        one_hour_later_date = self.date_time + datetime.timedelta(hours=1)
        one_hour_later_date = one_hour_later_date.replace(tzinfo=pytz.utc)
        other_message_options = dict(phone_no=other_phone_number, text=self.text_format % wakiso.name, received_at=one_hour_later_date,
                                     relayer_id=234, run_id=23243)
        user_profile = UserProfile(**dict(name='timothy', phone=other_phone_number, location=wakiso)).save()
        wakiso_message = RapidProMessage(**other_message_options).save()

        response = self.client.get(self.API_ENDPOINT, {"location": self.district.id, "format": "json"})

        wakiso_expected_message = {'phone': other_phone_number, 'time': one_hour_later_date, 'relayer': 234, 'run': 23243,
                                   'text': self.text_format % wakiso.name, 'disaster': None}
        wakiso_expected_message = dict(wakiso_expected_message.items() + {
            'source': user_profile.name,
            'id': str(wakiso_message.id),
            'location': str(wakiso),
            'profile_id': str(user_profile.id),
            'auto_associated': False}.items())

        bukoto_expected_message = dict(self.expected_message.items() + {
            'source': self.mobile_user.name,
            'id': str(bukoto_message.id),
            'disaster': None,
            'location': str(self.village),
            'profile_id': str(self.mobile_user.id),
            'auto_associated': False}.items())

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertEqual(wakiso_expected_message, response.data[0])
        self.assertEqual(bukoto_expected_message, response.data[1])

    @override_settings(REST_FRAMEWORK={})
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

    @override_settings(REST_FRAMEWORK={})
    def test_should_update_disaster_field_using_a_patch(self):
        message = RapidProMessage(**self.message).save()

        response = self.client.patch(self._api_url(message.id), data=dict(disaster=self.disaster.id))
        self.assertEqual(200, response.status_code)

        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())
        self.assertEqual(self.disaster, retrieved_message[0].disaster)

    @override_settings(REST_FRAMEWORK={})
    def test_should_update_disaster_field_with_post_is_also_supported_for_phantomjs_sake(self):
        message = RapidProMessage(**self.message).save()

        response = self.client.post(self._api_url(message.id), data=dict(disaster=self.disaster.id))
        self.assertEqual(200, response.status_code)

        retrieved_message = RapidProMessage.objects(**self.message)
        self.assertEqual(1, retrieved_message.count())
        self.assertEqual(self.disaster, retrieved_message[0].disaster)

    def test_should_filter_messages_by_disaster_association(self):
        self.message['text'] = 'unassociate-able disaster text text' #short circuit auto disaster association
        self.expected_message['text'] = 'unassociate-able disaster text text'
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

    def test_should_auto_associate_message_to_disaster(self):
        disaster_type = DisasterType(**dict(name='Flood', description="Some flood")).save()
        disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Flood",
                                  date=self.date_time,
                                  status="Assessment")
        kampala_disaster = Disaster(**disaster_attr).save()
        text = "NECOC.%s. flood here and allover the place!" % self.district.name
        self.message['text'] = text
        saved_message = RapidProMessage(**self.message).save()
        self.assertEqual(saved_message.disaster, kampala_disaster)

    def test_should_auto_associate_message_to_disaster_when_posted_from_subcounty(self):
        disaster_type = DisasterType(**dict(name='Flood', description="Some flood")).save()
        disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Flood",
                                  date=self.date_time,
                                  status="Assessment")
        kampala_disaster = Disaster(**disaster_attr).save()
        text = "NECOC.%s. flood here and allover the place!" % self.village.name
        self.message['text'] = text
        saved_message = RapidProMessage(**self.message).save()
        self.assertEqual(saved_message.disaster, kampala_disaster)

    def test_should_save_post_message_and_associate_to_disaster(self):
        disaster_type = DisasterType(**dict(name='Flood', description="Some flood")).save()
        disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Flood",
                                  date=self.date_time,
                                  status="Assessment")
        kampala_disaster = Disaster(**disaster_attr).save()
        text = "NECOC.%s. flood here and allover the place!" % self.district.name
        self.expected_message['text'] = text
        self.expected_message['time'] = self.date_time.strftime(RAPID_PRO_TIME_FORMAT)

        response = self.client.post(self.API_ENDPOINT, data=self.expected_message)
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data['disaster']['id'], str(kampala_disaster.id))

    @override_settings(REST_FRAMEWORK={
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_csv.renderers.CSVRenderer'
        ),
        "TEST_REQUEST_RENDERER_CLASSES": (
            'rest_framework_csv.renderers.CSVRenderer'
        )
    })
    def test_should_return_csv_when_csv_endpoint_is_called(self):
        disaster_type = DisasterType(**dict(name='Fire', description="Some fire")).save()
        disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Fire",
                                  date=self.date_time,
                                  status="Assessment")
        kampala_disaster = Disaster(**disaster_attr).save()

        msg = RapidProMessage(**self.message).save()
        expected_response = "phone,text,source,location,time,disaster\n" \
                            "+256775019449,NECOC.Bukoto. There is a fire,timothy,Kampala >> Bukoto,%s,Fire" % msg.received_at
        response = self.client.get(self.CSV_ENDPOINT, {'format': 'csv'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        # self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    def test_should_filter_csv_when_date_range_is_specified(self):
        new_date_time = datetime.datetime(2015, 9, 17, 16, 0, 49, 807000)
        new_date_time = new_date_time.replace(tzinfo=pytz.utc)
        disaster_type = DisasterType(**dict(name='Fire', description="Some fire")).save()
        disaster_attr = dict(name=disaster_type, locations=[self.district], description="Big Fire",
                                  date=self.date_time,
                                  status="Assessment")
        kampala_disaster = Disaster(**disaster_attr).save()

        RapidProMessage(**self.message).save()
        self.message['received_at'] = new_date_time
        RapidProMessage(**self.message).save()
        expected_response = "phone,text,source,location,time\n" \
                            "+256775019449,NECOC.Bukoto. There is a fire,timothy,Kampala >> Bukoto,%s,Fire" % self.date_time

        response = self.client.get(self.CSV_ENDPOINT, {'dfrom' : 'undefined', 'dto': '2014-11-26', 'format': 'csv'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

        response = self.client.get(self.CSV_ENDPOINT, {'dfrom' : '2015-01-01', 'dto': 'undefined', 'format': 'csv'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

        response = self.client.get(self.CSV_ENDPOINT, {'dfrom' : '2014-01-01', 'dto': '2014-11-26', 'format': 'csv'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

        response = self.client.get(self.CSV_ENDPOINT, {'dfrom' : '2014-01-01', 'dto': '2015-11-26', 'format': 'csv'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))

        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        # self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    def test_should_return_only_district_messages_for_CAO(self):
        self.mobile_user.user = self.cao_user
        self.mobile_user.save()

        masaka_district = Location(**dict(name='Masaka', parent=None, type='district')).save()
        masaka_village = Location(**dict(name='Bukasa', parent=masaka_district, type='village')).save()
        masaka_message = self.message.copy()
        masaka_message['location'] = masaka_village
        masaka_message['phone_no'] = "+256775019441"
        msk_msg = RapidProMessage(**masaka_message).save()
        kla_msg = RapidProMessage(**self.message).save()

        login_response = self.client.post(self.login_url, self.login_data)
        self.assertRedirects(login_response, '/')
        self.assertTrue('sessionid' in login_response.cookies)

        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.expected_message, response.data[0])
        self.assertEqual(self.mobile_user.name, response.data[0]['source'])
        self.assertEqual('Kampala >> Bukoto', response.data[0]['location'])
        self.assertIsNotNone(response.data[0]['id'])


import json
import datetime
import collections
from django.conf import settings
import mock
from mongoengine.django.auth import Group
from rest_framework_csv.renderers import CSVRenderer

from dms.models import Location, DisasterType, Disaster, User, UserProfile
from dms.tests.base import MongoAPITestCase
from dms.utils.rapidpro_message_utils import split_text


class TestDisasterEndpoint(MongoAPITestCase):

    API_ENDPOINT = '/api/v1/disasters/'
    CSV_ENDPOINT = '/api/v1/csv-disasters/'

    def setUp(self):
        self.user = self.login_user()
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.disaster_type = DisasterType(**dict(name="Fire", description="Fire"))
        self.disaster_type.save()
        self.disaster_type2 = DisasterType(**dict(name="Flood", description="Flood"))
        self.disaster_type2.save()
        self.disaster_to_post = dict(name=str(self.disaster_type.id), locations=[str(self.district.id)],
                                     description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")
        self.disaster = dict(name=self.disaster_type, locations=[self.district],
                             description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")

        self.mobile_user = UserProfile(**dict(name='timothy', phone="+256775019449",
                                             location=self.district, email=None)).save()
        self.cao_group, created = Group.objects.get_or_create(name='CAO')

    def test_should_post_a_disaster(self):
        response = self.client.post(self.API_ENDPOINT, data=json.dumps(self.disaster_to_post), content_type="application/json")
        self.assertEqual(201, response.status_code)

        retrieved_disaster = Disaster.objects(description="Big Flood")
        self.assertEqual(1, retrieved_disaster.count())

    def test_should_get_a_list_of_disasters(self):
        Disaster(**self.disaster).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.disaster_to_post['status'], response.data[0]['status'])
        self.assertEqual(self.disaster_to_post['date'], str(response.data[0]['date']))
        self.assertEqual(self.disaster_to_post['description'], response.data[0]['description'])

    def test_can_get_a_list_of_disasters_with_no_permissions(self):
        self.login_without_permissions()
        response = self.client.get(self.API_ENDPOINT)
        self.assertEquals(response.status_code, 200)

    def test_cant_post_to_disasters_without_permission(self):
        self.assert_permission_required_for_post(self.API_ENDPOINT)

    def test_can_post_to_disasters_with_permission(self):
        self.login_with_permission('can_manage_disasters')
        response = self.client.get(self.API_ENDPOINT)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(self.API_ENDPOINT, data=json.dumps(self.disaster_to_post), content_type="application/json")
        self.assertEqual(201, response.status_code)

    def test_should_get_a_single_disaster(self):
        disaster = Disaster(**self.disaster).save()
        response = self.client.get(self.API_ENDPOINT + str(disaster.id) + '/', format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.disaster_to_post['status'], response.data['status'])
        self.assertEqual(self.disaster_to_post['date'], str(response.data['date']))
        self.assertEqual(self.disaster_to_post['description'], response.data['description'])

    def test_cant_get_or_post_single_disaster_without_permission(self):
        disaster = Disaster(**self.disaster).save()
        self.assert_permission_required_for_get(self.API_ENDPOINT + str(disaster.id) + '/')
        self.assert_permission_required_for_post(self.API_ENDPOINT + str(disaster.id) + '/')

    def test_should_post_a_single_disaster(self):
        disaster = Disaster(**self.disaster_to_post).save()
        self.disaster_to_post['description'] = "Giant Flood"
        response = self.client.post(self.API_ENDPOINT + str(disaster.id) + '/',
                                    data=json.dumps(self.disaster_to_post),
                                    content_type="application/json")
        self.assertEqual(200, response.status_code)

        retrieved_disaster = Disaster.objects(description="Giant Flood")
        self.assertEqual(1, retrieved_disaster.count())

    def test_filter_disaster_by_status(self):
        Disaster(**self.disaster).save()
        disaster_attr2 = self.disaster.copy()
        disaster_attr2['status'] = "Closed"
        Disaster(**disaster_attr2).save()

        response = self.client.get(self.API_ENDPOINT+'?status=Closed&format=json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual('Closed', response.data[0]['status'])
        self.assertEqual(self.disaster_to_post['date'], str(response.data[0]['date']))
        self.assertEqual(self.disaster_to_post['description'], response.data[0]['description'])

    def test_filter_disaster_by_date(self):
        disaster_attr = self.disaster.copy()
        date_1_jan = "2014-01-01"
        disaster_attr['date'] = date_1_jan

        disaster_attr2 = self.disaster.copy()
        date_3_jan = "2014-01-03"
        disaster_attr2['date'] = date_3_jan

        Disaster(**disaster_attr).save()
        Disaster(**disaster_attr2).save()

        response = self.client.get(self.API_ENDPOINT+'?from=%s&to=%s&format=json' % (date_1_jan, date_3_jan))

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertEqual(datetime.datetime.strptime(date_1_jan, "%Y-%m-%d"), response.data[0]['date'])
        self.assertEqual(datetime.datetime.strptime(date_3_jan, "%Y-%m-%d"), response.data[1]['date'])

        response = self.client.get(self.API_ENDPOINT+'?from=%s&format=json' % date_3_jan)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(datetime.datetime.strptime(date_3_jan, "%Y-%m-%d"), response.data[0]['date'])

        response = self.client.get(self.API_ENDPOINT+'?to=%s&format=json' % date_1_jan)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(datetime.datetime.strptime(date_1_jan, "%Y-%m-%d"), response.data[0]['date'])

    def test_filter_disaster_by_date_and_date(self):
        disaster_attr = self.disaster.copy()
        date_1_jan = "2014-01-01"
        disaster_attr['date'] = date_1_jan

        disaster_attr2 = self.disaster.copy()
        date_3_jan = "2014-01-03"
        disaster_attr2['status'] = "Closed"
        disaster_attr2['date'] = date_3_jan

        Disaster(**disaster_attr).save()
        Disaster(**disaster_attr2).save()

        response = self.client.get(self.API_ENDPOINT+'?from=%s&to=%s&status=Closed&format=json' % (date_1_jan, date_3_jan))

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(datetime.datetime.strptime(date_3_jan, "%Y-%m-%d"), response.data[0]['date'])

        response = self.client.get(self.API_ENDPOINT+'?from=%s&status=closed&format=json' % date_3_jan)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(datetime.datetime.strptime(date_3_jan, "%Y-%m-%d"), response.data[0]['date'])

        response = self.client.get(self.API_ENDPOINT+'?to=%s&status=assessment&format=json' % date_1_jan)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(datetime.datetime.strptime(date_1_jan, "%Y-%m-%d"), response.data[0]['date'])

    def test_should_return_only_district_disasters_for_CAO(self):
        self.user.group = self.cao_group
        self.user.save()
        self.mobile_user.user = self.user
        self.mobile_user.save()

        masaka_district = Location(**dict(name='Masaka', parent=None, type='district')).save()

        masaka_disaster = dict(name=self.disaster_type, locations=[masaka_district],
                             description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")

        Disaster(**self.disaster).save()
        Disaster(**masaka_disaster).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.disaster_to_post['status'], response.data[0]['status'])
        self.assertEqual(self.disaster_to_post['date'], str(response.data[0]['date']))
        self.assertEqual(self.disaster_to_post['description'], response.data[0]['description'])
        self.assertEqual('Kampala', response.data[0]['locations'][0]['name'])

    def test_should_return_csv_when_csv_endpoint_is_called(self):
        Disaster(**self.disaster).save()
        disaster_attr2 = self.disaster.copy()
        disaster_attr2['status'] = "Closed"
        Disaster(**disaster_attr2).save()
        disaster2 = self.disaster.copy()
        disaster2['name'] = self.disaster_type2
        Disaster(**disaster2).save()

        response = self.client.get(self.CSV_ENDPOINT, format='csv')

        expected_response = "name,description,location,status,date\r\n" \
                            "Fire,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name,)
        expected_response = expected_response + "\r\nFire,Big Flood,%s,Closed,2014-12-01 00:00:00" % (self.district.name)
        expected_response = expected_response + "\r\nFlood,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    def test_should_return_filtered_csv_when_csv_endpoint_is_called(self):
        Disaster(**self.disaster).save()
        disaster_attr2 = self.disaster.copy()
        disaster_attr2['status'] = "Closed"
        Disaster(**disaster_attr2).save()
        disaster2 = self.disaster.copy()
        disaster2['name'] = self.disaster_type2
        sdisaster = Disaster(**disaster2).save()

        response = self.client.get(self.CSV_ENDPOINT, format='csv')

        expected_response = "name,description,location,status,date\r\n" \
                            "Fire,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name,)
        expected_response = expected_response + "\r\nFire,Big Flood,%s,Closed,2014-12-01 00:00:00" % (self.district.name)
        expected_response = expected_response + "\r\nFlood,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

        response = self.client.get(self.CSV_ENDPOINT + '?status=Assessment&from=undefined', format='csv')

        expected_response = "name,description,location,status,date\r\n" \
                            "Fire,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name,)
        expected_response = expected_response + "\r\nFlood,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

        sdisaster.date = "2014-12-02 00:00:00"
        sdisaster.save()

        response = self.client.get(self.CSV_ENDPOINT + '?status=Assessment&from=2014-12-02 00:00:00', format='csv')

        expected_response = "name,description,location,status,date\r\n" \
                            "Flood,Big Flood,%s,Assessment,2014-12-02 00:00:00" % (self.district.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

        response = self.client.get(self.CSV_ENDPOINT + '?to=2014-12-01 00:00:00', format='csv')

        expected_response = "name,description,location,status,date\r\n" \
                            "Fire,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name,)
        expected_response = expected_response + "\r\nFire,Big Flood,%s,Closed,2014-12-01 00:00:00" % (self.district.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    def test_should_return_csv_with_all_records_when_empty_filters_are_used_on_csv_endpoint(self):
        Disaster(**self.disaster).save()
        disaster_attr2 = self.disaster.copy()
        disaster_attr2['status'] = "Closed"
        Disaster(**disaster_attr2).save()
        disaster2 = self.disaster.copy()
        disaster2['name'] = self.disaster_type2
        sdisaster = Disaster(**disaster2).save()

        response = self.client.get(self.CSV_ENDPOINT + '?status=undefined&from=undefined&to=undefined', format='csv')

        expected_response = "name,description,location,status,date\r\n" \
                            "Fire,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name,)
        expected_response = expected_response + "\r\nFire,Big Flood,%s,Closed,2014-12-01 00:00:00" % (self.district.name)
        expected_response = expected_response + "\r\nFlood,Big Flood,%s,Assessment,2014-12-01 00:00:00" % (self.district.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    @mock.patch('dms.tasks.send_email.delay')
    def test_changing_disaster_status_sends_email_to_stakeholders(self, mock_send_email):
        disaster = Disaster(**self.disaster).save()
        disaster.status = 'Closed'
        disaster.save()
        mock_send_email.assert_called_with('Status of Disaster Risk has changed',
                                           mock.ANY,
                                           settings.DEFAULT_FROM_EMAIL,
                                           settings.DISASTER_NOTIFY_STATUS)

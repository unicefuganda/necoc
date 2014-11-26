import json
import datetime

from dms.models import Location, DisasterType, Disaster
from dms.tests.base import MongoAPITestCase


class TestDisasterEndpoint(MongoAPITestCase):

    API_ENDPOINT = '/api/v1/disasters/'

    def setUp(self):
        self.login_user()
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.disaster_type = DisasterType(**dict(name="Fire", description="Fire"))
        self.disaster_type.save()
        self.disaster_to_post = dict(name=str(self.disaster_type.id), locations=[str(self.district.id)],
                                     description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")
        self.disaster = dict(name=self.disaster_type, locations=[self.district],
                             description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")

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

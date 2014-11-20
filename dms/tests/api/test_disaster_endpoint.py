import json
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
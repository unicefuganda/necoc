import json
from dms.models import Location, DisasterType, Disaster
from dms.tests.base import MongoAPITestCase


class TestDisasterEndpoint(MongoAPITestCase):

    API_ENDPOINT = '/api/v1/disasters/'

    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.disaster_type = DisasterType(**dict(name="Fire", description="Fire"))
        self.disaster_type.save()
        self.disaster_to_post = dict(name=str(self.disaster_type.id), locations=[str(self.district.id)],
                                     description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")
        self.disaster = dict(name=self.disaster_type, locations=[self.district],
                             description="Big Flood", date="2014-12-01 00:00:00", status="Assessment")

    def test_should_post_a_mobile_user(self):
        response = self.client.post(self.API_ENDPOINT, data=json.dumps(self.disaster_to_post), content_type="application/json")
        self.assertEqual(201, response.status_code)

        retrieved_disaster = Disaster.objects(description="Big Flood")
        self.assertEqual(1, retrieved_disaster.count())

    def test_should_get_a_list_of_users(self):
        Disaster(**self.disaster).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.disaster_to_post['status'], response.data[0]['status'])
        self.assertEqual(self.disaster_to_post['date'], str(response.data[0]['date']))
        self.assertEqual(self.disaster_to_post['description'], response.data[0]['description'])
        # print response.data

        #
        # self.assertEqual(self.district.name, response.data[0]['location']['name'])
        # self.assertEqual(self.disaster_type.name, response.data[0]['name']['name'])
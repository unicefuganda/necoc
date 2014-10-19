from dms.models.disaster_type import DisasterType
from dms.tests.base import MongoAPITestCase


class TestDisasterTypeEndpoint(MongoAPITestCase):
    DISASTER_TYPE_ENDPOINT = '/api/v1/disaster-types/'

    def setUp(self):
        self.details = dict(name='Flood', description="water you can't drink")

    def test_should_post_a_disaster_type(self):
        response = self.client.post(self.DISASTER_TYPE_ENDPOINT, data=self.details)
        self.assertEqual(201, response.status_code)

        retrieved_user = DisasterType.objects(**self.details)
        self.assertEqual(1, retrieved_user.count())

    def test_should_get_a_list_of_users(self):
        DisasterType(**self.details).save()
        response = self.client.get(self.DISASTER_TYPE_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.details, response.data[0])
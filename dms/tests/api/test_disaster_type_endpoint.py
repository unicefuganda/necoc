from dms.models.disaster_type import DisasterType
from dms.tests.base import MongoAPITestCase


class TestDisasterTypeEndpoint(MongoAPITestCase):
    DISASTER_TYPE_ENDPOINT = '/api/v1/disaster-types/'

    def setUp(self):
        self.login_user()
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

    def test_can_get_a_list_of_disaster_types_with_no_permissions(self):
        response = self.client.get(self.DISASTER_TYPE_ENDPOINT)
        self.assertEquals(response.status_code, 200)

    def test_cant_post_to_disaster_types_without_permission(self):
        self.assert_permission_required_for_post(self.DISASTER_TYPE_ENDPOINT)

    def test_can_post_to_disaster_types_with_permission(self):
        self.login_with_permission('can_manage_disasters')
        response = self.client.get(self.DISASTER_TYPE_ENDPOINT)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(self.DISASTER_TYPE_ENDPOINT, data=self.details)
        self.assertEqual(201, response.status_code)

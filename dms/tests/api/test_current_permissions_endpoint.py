from dms.tests.base import MongoAPITestCase


class TestCurrentPermissionsEndpoint(MongoAPITestCase):

    API_ENDPOINT = '/api/v1/current-permissions/'

    def test_should_get_user_permissions_from_endpoint(self):
        self.login_with_permission('user_permission')
        response = self.client.get(self.API_ENDPOINT, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'permissions': ['user_permission']}, response.data)

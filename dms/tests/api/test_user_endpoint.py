from dms.models import Location
from dms.models.user import User
from dms.tests.base import MongoAPITestCase


class TestUserEndpoint(MongoAPITestCase):
    USER_ENDPOINT = '/api/v1/users/'

    def setUp(self):
        kampala = Location(name='Kampala', type='district').save()
        self.user_data = {
            'username': 'cage', 'first_name': 'nicolas', 'last_name': 'cage', 'email': 'nic@ol.as', 'password': 'haha',
            'phone_no': '235669502', 'location': str(kampala.id)
        }

    def test_should_get_current_user(self):
        user = User(**self.user_data).save()
        response = self.client.get(self.USER_ENDPOINT + '%s/' % str(user.id), format='json')

        self.assertEqual(200, response.status_code)
        expected_data = self.user_data.copy()
        del expected_data['password']
        del expected_data['location']

        self.assertDictContainsSubset(expected_data, response.data)

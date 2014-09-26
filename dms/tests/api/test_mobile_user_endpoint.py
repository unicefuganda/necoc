from dms.models.location import Location
from dms.models.mobile_user import MobileUser
from dms.tests.base import NoSQLAPITestCase


class TestMobileUserEndpoint(NoSQLAPITestCase):

    API_ENDPOINT = '/api/v1/mobile-users/'

    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.mobile_user_to_post = dict(name='timothy', phone='+256775019449', location=self.district.id, email=None)
        self.mobile_user = dict(name='timothy', phone='+256775019449', location=self.district, email=None)

    def tearDown(self):
        MobileUser.drop_collection()

    def test_should_post_a_mobile_user(self):
        response = self.client.post(self.API_ENDPOINT, data=self.mobile_user_to_post)
        self.assertEqual(201, response.status_code)

        retrieved_user = MobileUser.objects(name='timothy')
        self.assertEqual(1, retrieved_user.count())

    def test_should_get_a_list_of_users(self):
        MobileUser(**self.mobile_user).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.mobile_user_to_post['name'], response.data[0]['name'])
        self.assertEqual(self.mobile_user_to_post['phone'], response.data[0]['phone'])
        self.assertEqual(self.mobile_user_to_post['email'], response.data[0]['email'])
        self.assertEqual(self.district.name, response.data[0]['location']['name'])


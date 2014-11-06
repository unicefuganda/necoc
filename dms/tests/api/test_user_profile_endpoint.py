from mongoengine.django.auth import User
from dms.models.location import Location
from dms.models.user_profile import UserProfile
from dms.tests.base import MongoAPITestCase


class TestUserProfileEndpoint(MongoAPITestCase):

    API_ENDPOINT = '/api/v1/mobile-users/'

    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.mobile_user_to_post = dict(name='timothy', phone='+256775019449', location=self.district.id, email=None)
        self.mobile_user = dict(name='timothy', phone='+256775019449', location=self.district, email=None)

    def tearDown(self):
        UserProfile.drop_collection()

    def test_should_post_a_mobile_user(self):
        response = self.client.post(self.API_ENDPOINT, data=self.mobile_user_to_post)
        self.assertEqual(201, response.status_code)

        retrieved_user = UserProfile.objects(name='timothy')
        self.assertEqual(1, retrieved_user.count())

    def test_should_get_a_list_of_users(self):
        UserProfile(**self.mobile_user).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.mobile_user_to_post['name'], response.data[0]['name'])
        self.assertEqual(self.mobile_user_to_post['phone'], response.data[0]['phone'])
        self.assertEqual(self.mobile_user_to_post['email'], response.data[0]['email'])
        self.assertEqual(self.district.name, response.data[0]['location']['name'])

    def test_should_get_a_single_user(self):
        attr = self.mobile_user.copy()
        attr['user'] = User(username='cage', password='haha').save()
        profile = UserProfile(**attr).save()

        response = self.client.get(self.API_ENDPOINT + str(profile.id) + '/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mobile_user_to_post['name'], response.data['name'])
        self.assertEqual(self.mobile_user_to_post['phone'], response.data['phone'])
        self.assertEqual(self.mobile_user_to_post['email'], response.data['email'])
        self.assertEqual(self.district.name, response.data['location']['name'])
        self.assertEqual('cage', response.data['username'])

    def test_post_with_non_empty_username_creates_system_user(self):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'
        response = self.client.post(self.API_ENDPOINT, data=attr)
        self.assertEqual(201, response.status_code)

        retrieved_user_profile = UserProfile.objects(name='timothy')
        self.assertEqual(1, retrieved_user_profile.count())

        retrieved_user = User.objects(username='akampa')
        self.assertEqual(1, retrieved_user.count())
        self.assertEqual(retrieved_user.first(), retrieved_user_profile.first().user)

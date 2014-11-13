from django.conf import settings
import mock
from mongoengine.django.auth import Group
from dms.models import User, Location, UserProfile
from dms.tests.base import MongoAPITestCase


class TestUserProfileEndpoint(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/mobile-users/'

    def setUp(self):
        self.login_user()
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.mobile_user_to_post = dict(name='tim', phone='+256775019500', location=self.district.id, email='tim@akampa.com')
        self.mobile_user = dict(name='timothy', phone='+256775019449', location=self.district, email=None)

    def tearDown(self):
        UserProfile.drop_collection()

    def test_should_post_a_mobile_user(self):
        response = self.client.post(self.API_ENDPOINT, data=self.mobile_user_to_post)
        self.assertEqual(201, response.status_code)

        retrieved_user = UserProfile.objects(name='tim')
        self.assertEqual(1, retrieved_user.count())

    def test_should_get_a_list_of_users(self):
        UserProfile(**self.mobile_user).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.mobile_user['name'], response.data[0]['name'])
        self.assertEqual(self.mobile_user['phone'], response.data[0]['phone'])
        self.assertEqual(self.mobile_user['email'], response.data[0]['email'])
        self.assertEqual(self.district.name, response.data[0]['location']['name'])

    def test_raise_403_if_user_doesnt_have_manage_permission(self):
        self.assert_permission_required_for_get(self.API_ENDPOINT)
        self.assert_permission_required_for_post(self.API_ENDPOINT)

    def test_should_get_a_single_user(self):
        attr = self.mobile_user.copy()
        attr['user'] = User(username='cage', password='haha').save()
        profile = UserProfile(**attr).save()

        response = self.client.get(self.API_ENDPOINT + str(profile.id) + '/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mobile_user['name'], response.data['name'])
        self.assertEqual(self.mobile_user['phone'], response.data['phone'])
        self.assertEqual(self.mobile_user['email'], response.data['email'])
        self.assertEqual(self.district.name, response.data['location']['name'])
        self.assertEqual('cage', response.data['username'])

    def test_should_update_a_single_user(self):
        attr = self.mobile_user.copy()
        attr['email'] = 'tim@akampa.com'
        attr['phone'] = '+256775019500'
        attr['user'] = User(username='cage', password='haha').save()
        profile = UserProfile(**attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/', self.mobile_user_to_post)

        profile.reload()
        profiles = UserProfile.objects()
        self.assertEqual(1, profiles.count())

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mobile_user_to_post['name'], profile.name)
        self.assertEqual(self.mobile_user_to_post['phone'], profile.phone)
        self.assertEqual(self.mobile_user_to_post['email'], profile.email)

    def test_post_with_non_empty_username_creates_system_user(self):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'
        response = self.client.post(self.API_ENDPOINT, data=attr)
        self.assertEqual(201, response.status_code)

        retrieved_user_profile = UserProfile.objects(name='tim')
        self.assertEqual(1, retrieved_user_profile.count())

        retrieved_user = User.objects(username='akampa')
        self.assertEqual(1, retrieved_user.count())
        self.assertEqual(retrieved_user.first(), retrieved_user_profile.first().user)

    @mock.patch('dms.tasks.send_new_user_email.delay')
    def test_posting_new_system_user_sends_email(self, mock_send_new_user_email):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'
        attr['email'] = 'email@email.email'
        response = self.client.post(self.API_ENDPOINT, data=attr)
        self.assertEqual(201, response.status_code)
        mock_send_new_user_email.assert_called_with('Your NECOC Account',
                                                    mock.ANY,
                                                    settings.DEFAULT_FROM_EMAIL,
                                                    ['email@email.email'])
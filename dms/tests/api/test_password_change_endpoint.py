from django.conf import settings
import mock
from dms.models import User

from dms.models.location import Location
from dms.models.user_profile import UserProfile
from dms.tests.base import MongoAPITestCase


class TestPasswordChangeEndpoint(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/mobile-users/'

    def setUp(self):
        self.user = User(username='haha')
        self.initial_password = 'hehe'
        self.user.set_password(self.initial_password)
        self.password_data = dict(old_password=self.initial_password, new_password='hoho', confirm_password='hoho')
        self.district = Location(**dict(name='Kampala', type='district', parent=None)).save()
        self.mobile_user_attr = dict(name='tim', phone='+256775019500', location=self.district.id,
                                     email='tim@akampa.com', user=self.user)

    def test_should_update_password_of_user(self):
        profile = UserProfile(**self.mobile_user_attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/password/', self.password_data)

        profiles = UserProfile.objects()
        users = User.objects(username=self.user.username)

        self.assertEqual(200, response.status_code)
        self.assertEqual({}, response.data)
        self.assertEqual(1, profiles.count())
        self.assertEqual(1, users.count())
        self.assertTrue(users.first().check_password(self.password_data['new_password']))

        response = self.client.login(username=self.user.username, password=self.password_data['new_password'])
        self.assertTrue(response)

    def test_non_web_user_raises_404(self):
        attr = self.mobile_user_attr.copy()
        del attr['user']
        profile = UserProfile(**attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/password/', self.password_data)

        profiles = UserProfile.objects()
        users = User.objects(username=self.user.username)

        self.assertEqual(404, response.status_code)
        self.assertEqual({"detail": "Not found"}, response.data)
        self.assertEqual(1, profiles.count())
        self.assertEqual(1, users.count())
        self.assertTrue(users.first().check_password(self.password_data['old_password']))

    @mock.patch('dms.tasks.send_email.delay')
    def test_posting_new_password_sends_email(self, mock_send_email):
        profile = UserProfile(**self.mobile_user_attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/password/', self.password_data)
        self.assertEqual(200, response.status_code)
        mock_send_email.assert_called_with('Your NECOC Account',
                                           mock.ANY,
                                           settings.DEFAULT_FROM_EMAIL,
                                           [profile.email])

    def test_should_reset_password_of_user(self):
        profile = UserProfile(**self.mobile_user_attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/password_reset/', self.password_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual({}, response.data)
        self.assertFalse((User.objects(username=self.user.username)).first().check_password(self.initial_password))

    def test_reset_password_for_non_web_user_raises_404(self):
        attr = self.mobile_user_attr.copy()
        del attr['user']
        profile = UserProfile(**attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/password_reset/', self.password_data)
        self.assertEqual(404, response.status_code)
        self.assertEqual({"detail": "Not found"}, response.data)

    @mock.patch('dms.tasks.send_email.delay')
    def test_reseting_password_sends_email(self, mock_send_email):
        profile = UserProfile(**self.mobile_user_attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/password_reset/', self.password_data)
        self.assertEqual(200, response.status_code)
        mock_send_email.assert_called_with('NECOC Password Reset',
                                           mock.ANY,
                                           settings.DEFAULT_FROM_EMAIL,
                                           [profile.email])
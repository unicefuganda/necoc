import ast
from django.test import Client
from dms.models import User, UserProfile, Location
from dms.tests.base import MongoAPITestCase
from necoc import settings


class ProfileImageViewTest(MongoAPITestCase):

    PROFILE_IMAGE_ENDPOINT = '/api/v1/photo/'

    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.user_profile_attr = dict(name='timothy', phone='+256775019449', location=self.district, email=None)
        self.profile = UserProfile(**self.user_profile_attr)
        self.profile.photo.put(open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb'), content_type='image/content_type')
        self.profile.save()
        self.client = Client()
        self.login_user()

    def test_successfully_retrieve_profile_image(self):
        response = self.client.get(self.PROFILE_IMAGE_ENDPOINT + str(self.profile.id) + '/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb').read(), response.content)

    def test_not_permitted_to_view_profile(self):
        self.assert_permission_required_for_get(self.PROFILE_IMAGE_ENDPOINT + str(self.profile.id) + '/')

    def test_no_image_found(self):
        response = self.client.get(self.PROFILE_IMAGE_ENDPOINT + 'j34ks34344df234/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(open(settings.PROJECT_ROOT + '/../dms/client/app/img/default_profile.jpg', 'rb').read(), response.content)

    def test_allow_user_to_see_their_own(self):
        self.client.logout()
        attr = self.user_profile_attr.copy()
        attr['phone'] = '+2555837295789'
        user = User(username='someotheruser', email='emails@haha.com')
        user.group = None
        user.set_password('weak_password')
        attr['user'] = user
        profile = UserProfile(**attr)
        profile.photo.put(open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb'), content_type='image/content_type')
        profile.save()
        self.client.login(username='someotheruser', password='weak_password')

        response = self.client.get(self.PROFILE_IMAGE_ENDPOINT + str(profile.id) + '/')
        self.assertEquals(response.status_code, 200)

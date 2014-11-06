from django.test import Client
from mongoengine.django.auth import User
from dms.tests.base import MongoTestCase


class TestLogin(MongoTestCase):
    def setUp(self):
        self.login_url = '/login/'
        self.client = Client()

        user = User.objects.create(username='admin', email='admin@admin.admin')
        user.set_password('password')

    def test_should_get_login(self):
        response = self.client.get(self.login_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_should_redirect_to_index_page_when_successful_login(self):
        data = {
            'username': 'admin',
            'password': 'password'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, '/')
        self.assertTrue('sessionid' in response.cookies)

    def test_post_should_return_form_if_missing_data(self):
        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertEqual(2, len(form.errors))

    def test_post_should_return_form_if_invalid_user(self):
        data = {
            'username': 'admin',
            'password': 'not_password'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')
        errors = response.context['form'].errors
        self.assertEqual(1, len(errors))
        self.assertIn(u'Username or Password is invalid', errors['__all__'])


class TestLogout(MongoTestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create(username='admin', email='admin@admin.admin')
        user.set_password('password')

    def test_logging_user_out(self):
        self.client.login(username='admin', password='password')
        response = self.client.get('/logout/', follow=True)

        self.assertRedirects(response, '/login/')
        self.assertFalse('sessionid' in response.cookies)
from django.conf import settings
from django.test import Client
import mock
from dms.models import User
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
        form = response.context['login_form']
        self.assertEqual(2, len(form.errors))

    def test_post_should_return_form_if_invalid_user(self):
        data = {
            'username': 'admin',
            'password': 'not_password'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')
        errors = response.context['login_form'].errors
        self.assertEqual(1, len(errors))
        self.assertIn(u'Username or Password is invalid', errors['__all__'])

    @mock.patch('dms.tasks.send_email.delay')
    def test_should_email_password_reset_link_when_newpass_requested(self, mock_send_email):
        data = {
            'username': 'admin',
            'email': 'admin@admin.admin',
            'resetPass': 1,
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(200, response.status_code)
        mock_send_email.assert_called_with('NECOC Password Reset Request',
                                           mock.ANY,
                                           settings.DEFAULT_FROM_EMAIL,
                                           [data['email']])
        self.assertTemplateUsed(response, 'login.html')


    def test_should_return_form_with_errors_if_wrong_data_password_reset_data_submitted(self):
        data = {
            'username': 'badname',
            'password': 'poor.email',
            'resetPass': 1,
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertEqual(2, len(form.errors))


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
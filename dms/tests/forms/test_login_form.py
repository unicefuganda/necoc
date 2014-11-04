from dms.tests.base import MongoTestCase
from dms.forms.login_form import LoginForm


class LoginFormTest(MongoTestCase):
    def test_valid(self):
        form_data = {
            'username': 'some_user',
            'password': 'some_password'
        }
        login_form = LoginForm(form_data)
        self.assertTrue(login_form.is_valid())

    def test_invalid_without_username(self):
        form_data = {
            'password': 'some_password'
        }
        login_form = LoginForm(form_data)
        self.assertFalse(login_form.is_valid())

        errors = login_form.errors.as_data()
        self.assertEqual(str(errors['username'][0]), "[u'This field is required.']")

    def test_invalid_without_password(self):
        form_data = {
            'username': 'some_username'
        }
        login_form = LoginForm(form_data)
        self.assertFalse(login_form.is_valid())

        errors = login_form.errors.as_data()
        self.assertEqual(str(errors['password'][0]), "[u'This field is required.']")
from mock import patch
from dms.services.user_profile_service import UserProfileService
from dms.tests.base import MongoTestCase
from django.conf import settings


class UserProfileServiceTest(MongoTestCase):

    def setUp(self):
        pass

    @patch('django.core.mail.send_mail')
    @patch('mongoengine.django.auth.UserManager.make_random_password')
    def test_new_password_is_sent_in_email(self, mock_send_mail, mock_make_password):
        message = """
                Dear Andrew,

                Your email was recently registered for NECOC DMS.
                Please use the following credentials to login to http://

                username: andrew
                password: blabla

                Thank you,
                NECOC DMS team
                """
        mock_make_password.return_value = 'blabla'

        UserProfileService.setup_new_user('andrew', 'Andrew', 'andrew@some.where')

        self.assertTrue(mock_send_mail.called_once_with('Your NECOC Account',
                                                        message,
                                                        settings.DEFAULT_FROM_EMAIL,
                                                        ['andrew@some.where'],
                                                        fail_silently=False))

    @patch('django.core.mail.send_mail')
    def test_saves_new_password(self, mock_send_mail):
        user = UserProfileService.setup_new_user('andrew', 'Andrew', 'andrew@some.where')
        self.assertIsNotNone(user.password)
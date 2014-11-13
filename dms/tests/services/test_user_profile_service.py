from django.test import override_settings
from mock import patch
from dms.models import UserProfile
from dms.services.user_profile_service import UserProfileService
from dms.tests.base import MongoTestCase
from django.conf import settings


class UserProfileServiceTest(MongoTestCase):
    def setUp(self):
        pass

    @patch('mongoengine.django.auth.UserManager.make_random_password')
    @patch('dms.tasks.send_new_user_email.delay')
    @override_settings(NEW_USER_MESSAGE="%(name)s %(hostname)s %(username)s %(password)s")
    def test_new_password_is_sent_in_email(self, mock_send_mail, mock_make_password):
        message = "Andrew http://necoc.org.ug andrew blabla"
        mock_make_password.return_value = 'blabla'
        profile = UserProfile(name='Andrew', email='andrew@some.where')
        UserProfileService(profile).setup_new_user('andrew')
        mock_send_mail.assert_called_with('Your NECOC Account',
                                          message,
                                          settings.DEFAULT_FROM_EMAIL,
                                          ['andrew@some.where'])

    @patch('dms.tasks.send_new_user_email.delay')
    def test_setup_new_user_saves_new_password(self, mock_send_mail):
        profile = UserProfile(name='Andrew', email='andrew@some.where')
        user = UserProfileService(profile).setup_new_user('andrew')
        self.assertIsNotNone(user.password)

    @patch('dms.tasks.send_new_user_email.delay')
    @override_settings(CHANGE_PASSWD_MESSAGE="%(name)s %(hostname)s %(admin_email)s")
    @override_settings(ADMIN_EMAIL="")
    @override_settings(DEFAULT_FROM_EMAIL="alfred@al.fred")
    def test_password_change_notification_sends_email(self, mock_send_mail):
        message = "Andrew http://necoc.org.ug alfred@al.fred"
        profile = UserProfile(name='Andrew', email='andrew@some.where')
        UserProfileService(profile).notify_password_change()
        mock_send_mail.assert_called_with('Your NECOC Account',
                                          message,
                                          "alfred@al.fred",
                                          ['andrew@some.where'])

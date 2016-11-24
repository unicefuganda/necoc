from dms.models import User
from mongoengine.django.auth import UserManager

from dms.tasks import send_email, send_one_sms
from django.conf import settings


class UserProfileService(object):

    def __init__(self, profile):
        self.profile = profile

    def setup_new_user(self, username, group_id):
        user = User(username=username, group=group_id).save()
        password = self.set_new_password(user)
        message = self._build_new_user_email_message(username, password)
        send_email.delay('Your NECOC Account', message, settings.DEFAULT_FROM_EMAIL, [self.profile.email])
        if self.profile.phone and getattr(settings, 'SENDSMS_ON_PASSWORD_RESET', False):
            text = 'Your NECOC password for user: %s has been set to %s' % (username, password)
            send_one_sms.delay(None, self.profile.phone, text)
        return user

    def reset_password(self):
        user = self.profile.user
        password = self.set_new_password(user)
        message = self._build_reset_password_message(password)
        user.save()
        self.profile.save()
        send_email.delay('NECOC Password Reset', message, settings.DEFAULT_FROM_EMAIL, [self.profile.email])

    def notify_password_change(self):
        message = self._build_change_password_notification_message()
        send_email.delay('Your NECOC Account', message, settings.DEFAULT_FROM_EMAIL, [self.profile.email])

    @classmethod
    def set_new_password(cls, user):
        password = UserManager().make_random_password()
        user.set_password(password)
        return password

    def _build_new_user_email_message(self, username, password):
        params = {'name': self.profile.name, 'hostname': settings.HOSTNAME,
                  'username': username, 'password': password}
        return settings.NEW_USER_MESSAGE % params

    def _build_reset_password_message(self, password):
        params = {'name': self.profile.name,
                  'password': password,
                  'hostname': settings.HOSTNAME,
                  'admin_email': settings.ADMIN_EMAIL or settings.DEFAULT_FROM_EMAIL}
        return settings.RESET_PASSWORD_MESSAGE % params

    def _build_change_password_notification_message(self):
        params = {'name': self.profile.name, 'hostname': settings.HOSTNAME,
                  'admin_email': settings.ADMIN_EMAIL or settings.DEFAULT_FROM_EMAIL}
        return settings.CHANGE_PASSWD_MESSAGE % params

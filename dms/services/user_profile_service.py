from dms.models import User
from mongoengine.django.auth import UserManager

from dms.tasks import send_new_user_email
from django.conf import settings


class UserProfileService(object):

    def __init__(self, profile):
        self.profile = profile

    def setup_new_user(self, username):
        user = User(username=username).save()
        password = self.set_new_password(user)
        message = self.build_email_message(username, password)
        send_new_user_email.delay('Your NECOC Account', message, settings.DEFAULT_FROM_EMAIL, [self.profile.email])
        return user

    @classmethod
    def set_new_password(cls, user):
        password = UserManager().make_random_password()
        user.set_password(password)
        return password

    def build_email_message(self, username, password):
        params = {'name': self.profile.name, 'hostname': settings.HOSTNAME,
                  'username': username, 'password': password}
        return settings.NEW_USER_MESSAGE % params
